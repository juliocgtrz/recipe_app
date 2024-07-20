from io import BytesIO
import base64
import matplotlib.pyplot as plt

#defines function to create graph
def get_graph():
    #creates a BytesIO buffer for the image
    buffer = BytesIO()

    #creates plot with a BytesIO object as a file-like object
    plt.savefig(buffer, format="png")

    #sets cursor to beginning of the stream
    buffer.seek(0)

    #retrieves content of the file
    image_png = buffer.getvalue()

    #encodes the bytes-like object
    graph = base64.b64encode(image_png)

    #decodes to get the string as output
    graph = graph.decode("utf-8")

    #frees up the memory of buffer
    buffer.close()

    #returns the image/graph
    return graph

#defines function to implement logic to prepare the chart based on user input
def get_chart(chart_type, data, **kwargs):
    #switches plot backend to Anti-Grain Geometry to write to file
    plt.switch_backend("AGG")

    #specifies figure size
    fig = plt.figure(figsize=(6,3))

    #determines layout of each chart_type
    if chart_type == "#1":
        #plots bar chart between recipe name on x-axis and cooking_time on y-axis
        plt.bar(data["name"], data["cooking_time"])
        plt.xlabel("Recipe Names")
        plt.ylabel("Cooking Time (Minutes)")
        plt.xticks(rotation=45, ha="right")

    elif chart_type == "#2":
        #generates pie chart based on difficulty with difficulties as labels
        labels = data["difficulty"].value_counts().index
        sizes = data["difficulty"].value_counts().values
        plt.pie(sizes, labels=labels, autopct="%1.1f%%")

    elif chart_type == "#3":
        #plots line chart between recipe name on x-axis and number of ingredients on y-axis
        plt.plot(data["name"], data["number_of_ingredients"], marker="o")
        plt.xlabel("Recipes Names")
        plt.ylabel("Number of Ingredients")
        plt.xticks(rotation=45, ha="right")

    else:
        print("Unknown chart type")

    #specifies layout details
    plt.tight_layout()

    #returns the graph to file
    chart = get_graph()
    return chart