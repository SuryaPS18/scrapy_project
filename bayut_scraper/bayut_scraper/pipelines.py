# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BayutScraperPipeline:
    def process_item(self, item, spider):
        return item


import mysql.connector

class MySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'w@1806Djkq#',
            database = 'mybayutdatas'
        )
        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS mybayutdatas(
            id int NOT NULL auto_increment,
            property_id VARCHAR(255),
            purpose VARCHAR(255),
            type VARCHAR(255),
            added_on VARCHAR(255),
            furnishing VARCHAR(255),
            price INTEGER,
            location VARCHAR(255),
            bed_bath_size INTEGER,
            agent_name VARCHAR(255),
            img_url VARCHAR(255),
            description text,
            PRIMARY KEY (id)


        )
        """)

    def process_item(self,item,spider):
        self.cur.execute(""" insert into mybayutdatas (
            property_id,
            purpose,
            type,
            added_on,
            furnishing,
            price,
            location,
            bed_bath_size,
            agent_name,
            img_url,
            description,

            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,

                )""",(
            item["property_id"],
            item["purpose"],
            item["type"],
            item["added_on"],
            item["furnishing"],
            item["price"],
            item["location"],
            item["bed_bath_size"],
            item["agent_name"],
            item["img_url"],
            item["description"]
            
        ))
         
        self.conn.commit()
        return item
    
    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()