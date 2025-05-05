import os
import uuid
from rutube import Rutube


async def get_rutube_file(user_id,url):
    rt = Rutube(url)
    print(rt.playlist)
    rt.get_worst().download(path=f'media/{user_id}/')
    end_name = f'media/{user_id}/{uuid.uuid4()}.mp4'
    os.rename(f'media/{user_id}/{rt.playlist[0]}.mp4', end_name)
    return end_name
