import speedtest
import asyncio


def humansize(nbytes, pretty: bool = True):
    suffixes = ['b', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb']
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i]) if pretty else f


async def measure_speed(mode: str = "download", pretty: bool = False) -> str | float:
    """Измеряет скорость сети (download, upload)."""

    loop = asyncio.get_event_loop()
    mode = mode.lower()

    try:
        st = speedtest.Speedtest(secure=True)
        st.get_best_server()
    except speedtest.ConfigRetrievalError as e:
        raise ValueError(f"HTTP Error 403: Forbidden. Details: {str(e)}")

    if mode == "download":
        result = await loop.run_in_executor(None, st.upload)
    elif mode == "upload":
        result = await loop.run_in_executor(None, st.download)
    else:
        raise ValueError("Invalid mode. Use 'download' or 'upload'.")

    result /= 8

    return humansize(result, True) if pretty else result


def speed_test() -> (str, str):
    st = speedtest.Speedtest(secure=True)
    st.get_best_server()
    st.download()
    st.upload()
    results = st.results.dict()

    return humansize(results["download"]), humansize(results["upload"])
