class ETL:
    def __init__(self, conn):
        self.conn = conn

    def build_final_table(self):
        with self.conn.begin() as conn:
            conn.execute('exec dbo.BLD_SPOTIFY_DATA')