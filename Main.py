import serial, time, statistics, math, Veg_price_scrape, difflib, random, pickle


class Interface:
    def __init__(self):
        # Load the previous data from the pickled file first
        with open('data.pkl', 'rb') as p_r_file:
            self.data_dict = pickle.load(file=p_r_file)

        # Ready the previous day's height from the saved data in file
        self.prev_day_height = self.data_dict['Height']
        self.prev_week_leftover = self.data_dict['Week_Leftover']
        self.max_height = self.data_dict['Max_Height']

        self.url = 'http://www.truetamil.in/price/vegetable-price-bangalore.php'
        self.day_count = 0
        self.week_count = 0
        self.shelf_life_dict = {}
        self.veg_price_dict = {}
        self.potato_price = None
        self.veg_density = 1.08
        self.original_veg_name = 'potato'
        self.renew_period = 7  # Days
        self.veg_stock_period = random.choice([8, 12, 9, 10, 20])
        self.d_height = 0
        self.bucket_radius = 11
        self.shelf_life = None
        self.sensor_height = 35
        self.renew_height_threshold = self.max_height / 2
        self.height = 0

    def main(self):
        # Read the input from the serial port
        ser = serial.Serial(port='COM3', baudrate=9600)
        time.sleep(3)
        ser.write('S'.encode())

        read_list = []
        # Read values continuously
        for i in range(10):
            try:
                # convert the read binary value to normal ASCII string
                serial_read = ser.readline().decode('ascii').rstrip()
                read_list.append(float(serial_read))
                # Wait for the next data
                time.sleep(0.25)

            except Exception as e:
                # Exception Handler
                print(e)
                time.sleep(0.25)

        # Remove unwanted distance data
        read_list = [float(i) for i in read_list if i < 100 and i > 6]

        try:
            # Calculate the mean of all the valid distance data
            self.height = statistics.mean(read_list)
        except Exception as e:
            # If any error is generated, initialize mean value to 0
            print(e)

        # Find the height of the vegetable from the base of the container
        self.height = self.sensor_height - self.height

        if self.height < 0:
            self.height = 0

        # Load the shelf life information
        with open('veg_shelf_life.csv', 'r') as file:
            veg_shelf_data = file.read()

        for line in veg_shelf_data.split('\n')[:-1]:
            self.shelf_life_dict[line.split(',')[0]] = int(line.split(',')[1])

        # Web scrape the prices of the vegetables from the url
        self.veg_price_dict = Veg_price_scrape.veg_prices(self.url)

        # Get the closest matching vegetable name in the list and Find it's price
        # This step is necessary because the website might have a different variety of name for the vegetable
        veg_name = difflib.get_close_matches(self.original_veg_name, iter(self.veg_price_dict))[0]
        self.potato_price = self.veg_price_dict[veg_name]

        # Day counter resets every 7 days
        if self.day_count == self.renew_period:
            self.day_count = 0

        # Compute the increase in height by subtracting the previous height from the current height
        self.d_height = self.height - self.prev_day_height

        # If vegetable has been reduced, the height added is taken as 0
        if self.d_height < 0:
            self.d_height = 0

        # Calculate the Volume from given self.height (Volume of cylinder)
        veg_volume = math.pi * self.bucket_radius ** 2 * self.height
        max_volume = math.pi * self.bucket_radius ** 2 * self.max_height

        # Calculate vegetable weight and Convert weight in grams to KG
        veg_weight = (self.veg_density * veg_volume) / 1000
        max_weight = (self.veg_density * max_volume) / 1000

        # Calculate the cost of the amount of potato
        potato_cost = veg_weight * self.potato_price

        # Coming week weight and price estimates
        coming_week_weight_req_estimate = max_weight - self.prev_week_leftover
        coming_week_price_estimate = coming_week_weight_req_estimate * self.potato_price

        # Get the Vegetable shelf life from the CSV file
        veg_name_shelf = difflib.get_close_matches(self.original_veg_name, iter(self.shelf_life_dict))[0]
        self.shelf_life = self.shelf_life_dict[veg_name_shelf]

        # Debugging step ------ REMOVE
        print('Data Input:', read_list)
        print('Veg Weight:', veg_weight)
        print('Mean Height:', self.height)
        print('Potato Cost:', potato_cost)
        print('Next week weight estimate:', coming_week_weight_req_estimate)
        print('Next week Price estimate:', coming_week_price_estimate)
        print('Shelf Life:', self.shelf_life)
        print('Vegetable stock period:', self.veg_stock_period)
        print('Vegetable added:', self.d_height)

        # Conditions to check if the vegetable is rotten or if the vegetable has been renewed or not
        if self.veg_stock_period > self.shelf_life:
            print("Warning! Rotten Vegetable! Remove!")

        elif self.veg_stock_period > self.shelf_life - 2:
            print("Warning! Vegetable going to rot!")

        if self.d_height > self.renew_height_threshold:
            # self.data_dict['Max_Height'] = self.height
            print("Renewed!")

        if self.height < 0.1 * self.max_height or self.day_count == 6:
            print("Order new Vegetables!")

        if self.day_count == 6:
            # self.data_dict['Week_Leftover'] = self.height
            pass

        # self.data_dict['Height'] = self.height

        # Increment day count and week count with every iteration
        self.day_count += 1
        if self.day_count == self.renew_period:
            self.week_count += 1

        print('Week:', self.week_count + 1)
        print('Day:', self.day_count + 1)
        print('Done!\n')

        return_data = [self.height, self.potato_price, potato_cost,
                       coming_week_weight_req_estimate, coming_week_price_estimate,
                       self.prev_day_height, self.max_height, veg_weight]

        # Rounding off the data
        return_data = [math.ceil(i * 100) / 100 for i in return_data]

        # Save the new data for following days
        with open('data.pkl', 'wb') as p_w_file:
            pickle.dump(obj=self.data_dict, file=p_w_file)

        return return_data


if __name__ == '__main__':
    obj = Interface()
    new = obj.main()
    print(new)
