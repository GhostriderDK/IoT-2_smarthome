import sqlite3

def get_stue_data(number_of_rows):
    while True:
        query = """SELECT * FROM stue ORDER BY datetime DESC;"""
        datetimes = []
        temperatures = []
        humidities = []
        tvoc = []
        particles =  []
        co2 = []
        try:
            conn = sqlite3.connect("database/data.db")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(number_of_rows)
            for row in reversed(rows):
                datetimes.append(row[0])
                temperatures.append(row[1])
                humidities.append(row[2]) 
                tvoc.append(row[3])
                particles.append(row[4])
                co2.append(row[5])
            return datetimes, temperatures, humidities, tvoc, particles, co2         
        except sqlite3.Error as sql_e:
            print(f"sqlite error occurred: {sql_e}")
            conn.rollback()

        except Exception as e:
            print(f"Another error occured: {e}")
        finally:
            conn.close()


get_stue_data(10)

def get_bath_data(number_of_rows):
    while True:
        query = """SELECT * FROM bad ORDER BY datetime DESC;"""
        datetimes = []
        temperatures = []
        humidities = []
        battery = []
        try:
            conn = sqlite3.connect("database/data.db")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(number_of_rows)
            for row in reversed(rows):
                datetimes.append(row[0])
                temperatures.append(row[1])
                humidities.append(row[2]) 
                battery.append(row[3])
            return datetimes, temperatures, humidities, battery           
        except sqlite3.Error as sql_e:
            print(f"sqlite error occurred: {sql_e}")
            conn.rollback()

        except Exception as e:
            print(f"Another error occured: {e}")
        finally:
            conn.close()


get_bath_data(10)

def get_bedroom_data(number_of_rows):
    while True:
        query = """SELECT * FROM bedroom ORDER BY datetime DESC;"""
        datetimes = []
        temperatures = []
        humidities = []
        battery = []
        try:
            conn = sqlite3.connect("database/data.db")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(number_of_rows)
            for row in reversed(rows):
                datetimes.append(row[0])
                temperatures.append(row[1])
                humidities.append(row[2]) 
                battery.append(row[3])
            return datetimes, temperatures, humidities, battery           
        except sqlite3.Error as sql_e:
            print(f"sqlite error occurred: {sql_e}")
            conn.rollback()

        except Exception as e:
            print(f"Another error occured: {e}")
        finally:
            conn.close()



get_bedroom_data(10)