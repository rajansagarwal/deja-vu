import psycopg2
from datetime import datetime
from dotenv import dotenv_values


class PostgresUploader:
    def __init__(self, url):
        self.url = url

    def create_table(self):
        try:
            # Connect to the database
            conn = psycopg2.connect(self.url)
            cursor = conn.cursor()

            # Prepare the SQL statement to create the table if it doesn't exist
            create_table_sql = """
                CREATE TABLE IF NOT EXISTS chunks (
                    id SERIAL PRIMARY KEY,
                    vid_url TEXT NOT NULL,
                    upload_time TIMESTAMP NOT NULL,
                    audio_text TEXT,
                    audio_vector BYTEA,
                    clip_text TEXT,
                    clip_vector BYTEA,
                    start_time TIMESTAMP
                )
            """

            # Execute the SQL statement to create the table
            cursor.execute(create_table_sql)

            # Commit the transaction
            conn.commit()

            print("Table created successfully.")
        except psycopg2.Error as e:
            print("Error creating table:", e)

    def upload_chunk(self, vid_url, audio_text, audio_vector, clip_text, clip_vector, start_time):
        try:
            # Connect to the database
            conn = psycopg2.connect(self.url)
            cursor = conn.cursor()

            # Prepare the SQL statement
            sql = "INSERT INTO chunks (vid_url, upload_time, audio_text, audio_vector, clip_text, clip_vector, start_time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            timestamp = datetime.now()

            # Execute the SQL statement
            cursor.execute(sql, (vid_url, timestamp, audio_text, audio_vector, clip_text, clip_vector, start_time))

            # Commit the transaction and close the connection
            conn.commit()
            conn.close()

            print("Chunk uploaded successfully.")
        except psycopg2.Error as e:
            print("Error uploading chunk:", e)

    def get_chunk_data(self, chunk_id):
        try:
            # Connect to the database
            conn = psycopg2.connect(self.url)
            cursor = conn.cursor()

            # Prepare the SQL statement
            sql = "SELECT id, vid_url, upload_time, audio_text, clip_text, start_time FROM chunks WHERE id = %s"

            # Execute the SQL statement
            cursor.execute(sql, (chunk_id,))

            # Fetch the result
            result = cursor.fetchone()

            # Close the connection
            conn.close()

            if result:
                chunk_data = {
                    "id": result[0],
                    "vid_url": result[1],
                    "upload_time": result[2],
                    "audio_text": result[3],
                    "clip_text": result[4],
                    "start_time": result[5]
                }
                return chunk_data
            else:
                return None
        except psycopg2.Error as e:
            print("Error retrieving chunk data:", e)
    
    


env_config = dotenv_values(".env")
cock_url = env_config.get('COCK_URL')

url = cock_url

dbuploader = PostgresUploader(url)
dbuploader.create_table()
dbuploader.upload_chunk("joemama.com", "audio_text", b"audio_vector", "clip_text", b"clip_vector", datetime.now())
chunk_data = dbuploader.get_chunk_data(1)
print(chunk_data)