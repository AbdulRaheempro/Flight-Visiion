import mysql.connector
import pandas as pd 

class db:

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='airport'
            )
            self.mycursor = self.conn.cursor()
            print("connection established")
        except Exception as e:
            print('error:', e)

    def fetchcityname(self):
        city = []
        self.mycursor.execute("""
            SELECT DISTINCT(source_city) FROM pflight
            UNION
            SELECT DISTINCT(destination_city) FROM pflight
        """)
        data = self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
        return city

    def fetchallflight(self, source, destination):
        self.mycursor.execute("""
            SELECT airline, flight, departure_time, class, price
            FROM pflight
            WHERE source_city=%s AND destination_city=%s
        """, (source, destination))
        
        rows = self.mycursor.fetchall()
        col_names = [desc[0] for desc in self.mycursor.description]
        
        df = pd.DataFrame(rows, columns=col_names)
        return df
    
    def fetchairlinefreq(self):
       airline = []
       freq = []  # This is the correct variable name

       self.mycursor.execute("""
        SELECT airline, COUNT(*) 
        FROM pflight
        GROUP BY airline
    """)

       data = self.mycursor.fetchall()
       for i in data:
          airline.append(i[0])
          freq.append(i[1])  # Corrected here

       return airline, freq
   
    def busyairport(self):
        city=[]
        freq=[]
        self.mycursor.execute(
            """
            SELECT source_city, COUNT(*)
              FROM (
         SELECT source_city FROM pflight
        UNION ALL
       SELECT destination_city FROM pflight
       ) AS combined
       GROUP BY source_city
       order by COUNT(*) desc"""
        )
        data = self.mycursor.fetchall()
        for i in data:
          city.append(i[0])
          freq.append(i[1])  # Corrected here

        return city, freq
    
    def avgprice_per_airline(self):
      airline = []
      avg_price = []
      self.mycursor.execute("""
        SELECT airline, AVG(price) 
        FROM pflight
        GROUP BY airline
    """)
      data = self.mycursor.fetchall()
      for row in data:
        airline.append(row[0])
        avg_price.append(round(row[1], 2))
      return airline, avg_price


    def flights_per_class(self):
      classes = []
      freq = []
      self.mycursor.execute("""
        SELECT class, COUNT(*) 
        FROM pflight
        GROUP BY class
      """)
      data = self.mycursor.fetchall()
      for row in data:
        classes.append(row[0])
        freq.append(row[1])
      return classes, freq


