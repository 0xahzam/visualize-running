import math
from pathlib import Path
import gpxpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def process_file(fpath):
    if str(fpath).endswith(".gpx"):
        return process_gpx(fpath)


def process_gpx(gpxfile):
    with open(gpxfile, encoding="utf-8") as f:
        try:
            activity = gpxpy.parse(f)
        except gpxpy.mod_gpx.GPXException as e:
            print(f"\nSkipping {gpxfile}: {type(e).__name__}: {e}")
            return None

    lon = []
    lat = []
    ele = []
    time = []
    name = []
    dist = []

    for activity_track in activity.tracks:
        for segment in activity_track.segments:
            x0 = activity.tracks[0].segments[0].points[0].longitude
            y0 = activity.tracks[0].segments[0].points[0].latitude
            d0 = 0
            for point in segment.points:
                x = point.longitude
                y = point.latitude
                z = point.elevation
                t = point.time
                lon.append(x)
                lat.append(y)
                ele.append(z)
                time.append(t)
                name.append(gpxfile)
                d = d0 + math.sqrt(math.pow(x - x0, 2) + math.pow(y - y0, 2))
                dist.append(d)
                x0 = x
                y0 = y
                d0 = d

    df = pd.DataFrame(
        list(zip(lon, lat, ele, time, name, dist)),
        columns=["lon", "lat", "ele", "time", "name", "dist"],
    )

    return df


def process_data(path):
    print("Processing all GPX files in the folder...")
    folder_path = Path(path)
    filenames = folder_path.glob("*.gpx")
    processed = []
    for filename in filenames:
        result = process_file(filename)
        if result is not None:
            processed.append(result)

    df = pd.concat(processed)

    df["time"] = pd.to_datetime(df["time"], utc=True)

    print(df)
    return df


def plot_facets(df, output_file="plot.png"):
    # Create a new figure
    plt.figure()

    # Compute activity start times (for facet ordering)
    start_times = (
        df.groupby("name").agg({"time": "min"}).reset_index().sort_values("time")
    )

    ncol = math.ceil(math.sqrt(len(start_times)))

    # Create facets
    p = sns.FacetGrid(
        data=df,
        col="name",
        col_wrap=ncol,
        col_order=start_times["name"],
        sharex=False,
        sharey=False,
    )

    # Add activities
    p = p.map(plt.plot, "lon", "lat", color="black", linewidth=4)

    # Update plot aesthetics
    p.set(xlabel=None)
    p.set(ylabel=None)
    p.set(xticks=[])
    p.set(yticks=[])
    p.set(xticklabels=[])
    p.set(yticklabels=[])
    p.set_titles(col_template="", row_template="")
    sns.despine(left=True, bottom=True)
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
    plt.savefig(output_file)


df = process_data("gpx")
outfile = f"test-facets.png"
plot_facets(df, output_file=outfile)
print(f"Saved to {outfile}")
