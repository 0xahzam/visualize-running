import math
import gpxpy
import pandas as pd
import matplotlib.pyplot as plt


def plot_facets(df, output_file="plot.png"):
    plt.figure()
    plt.plot(df["lon"], df["lat"], color="black", linewidth=4)
    plt.axis("off")
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.savefig(output_file)


def gpxParse(file):
    file = open(gpxfile, encoding="utf-8")
    activity = gpxpy.parse(file)

    lon, lat, ele, time, name, dist = [], [], [], [], [], []

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


gpxfile = "test.gpx"
df = gpxParse(gpxfile)
plot_facets(df, output_file="simple-output")
