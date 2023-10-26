from database import Base, SessionLocal, engine
import pandas as pd


def batch_load_sql(query: str) -> pd.DataFrame:

    CHUNKSIZE = 1000
    conn = engine.connect().execution_options(stream_results=True)
    chunks = []
    for chunk_dataframe in pd.read_sql(query, conn,
                                       chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)
        print(chunk_dataframe)
    conn.close()
    data = pd.concat(chunks, ignore_index=True)

    return data

def load_features() -> pd.DataFrame:
    query = "v_patrakeev_all_posts_new"
    query2 = "v_patrakeev_all_users_new"
    return batch_load_sql(query), batch_load_sql(query2)

