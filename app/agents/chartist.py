import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

async def run_chartist(historical_data: list[dict]) -> str:
    """
    Returns a base64 encoded image string that can be loaded in a web app.
    """
    print("Chartist Agent: Starting chart generation...")
    if not historical_data:
        print("Chartist Agent: No data provided.")
        return ""

    df = pd.DataFrame(historical_data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['close'], marker='o', linestyle='-', color='b')
    plt.title('Stock Price Over Last 100 Days')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()


    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    print("Chartist Agent: Finished chart generation.")
    return image_base64