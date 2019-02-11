import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def graficarHistograma(data, column):
    plt.figure(figsize=(4,4))
    data[column].hist( bins=6, alpha=1, edgecolor = 'black',  linewidth=1, align= "mid" )
    plt.show()

def graficarTorta(title, sizes, tags, legend_title):
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    wedges, texts,autotexts = ax.pie(sizes, autopct=lambda pct: func(pct, sizes),
                                    textprops=dict(color="w"))
    ax.legend(wedges, tags,
            title= legend_title,
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=15, weight="bold")

    fontdict = {'fontsize': 20,
                'verticalalignment': 'baseline'}
    ax.set_title(title, fontdict = fontdict)

    plt.show()

def graficarBarchart_gendertopic():
    data.topic.unique()
    male_data = data[data["gender"] == 'male']
    female_data = data[data["gender"] == 'female']
    male_count, female_count = pd.Series([]), pd.Series([])

    for topic in data.topic.unique():
        male_count = male_count.append(pd.Series([male_data[male_data["topic"] == topic].gender.count()]), ignore_index=True)
        female_count = female_count.append(pd.Series(female_data[female_data["topic"] == topic].gender.count()), ignore_index=True)

    final_data = pd.DataFrame({"Tema": data.topic.unique(), "Hombres": male_count, "Mujeres": female_count})
    final_data = final_data.sort_values(by = ["Hombres", "Mujeres"], ascending = False)
    final_data = final_data.head(10)


    men_data = list(final_data["Hombres"])
    women_data = list(final_data["Mujeres"])

    ind = np.arange(len(men_data))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(20, 10))
    rects1 = ax.bar(ind - width/2, men_data, width,
                    color='SkyBlue', label='Hombres')
    rects2 = ax.bar(ind + width/2, women_data, width,
                    color='IndianRed', label='Mujeres')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Publicaciones')
    ax.set_title('Temas de publicacion segun el genero')
    ax.set_xticks(ind)
    ax.set_xticklabels(data.topic.unique(), rotation=45)
    ax.legend()


    def autolabel(rects, xpos='center'):
        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.1, 'left': 0.9}  # x_txt = x + w*off

        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')
            ax.major_label_orientation = "vertical"

    autolabel(rects1, "left")
    autolabel(rects2, "right")
    plt.show()
def graficarBarchart_agevstopic():
        df = data[['age','topic']]
        df_new = pd.DataFrame(columns =["10-20", "20-30","30-40","40-50"], index = [df.topic.unique()])
        for topic in df.topic.unique():
                df1020 = df.query("(age >= 10 & age < 20) & topic == '{}'".format(topic))["age"].count()
                df2030 = df.query("(age >= 20 & age < 30) & topic == '{}'".format(topic))["age"].count()
                df3040 = df.query("(age >= 30 & age < 40) & topic == '{}'".format(topic))["age"].count()
                df4050 = df.query("(age >= 40) & topic == '{}'".format(topic))["age"].count()
                df_new.at[topic, "10-20"] = df1020
                df_new.at[topic, "20-30"] = df2030
                df_new.at[topic, "30-40"] = df3040
                df_new.at[topic, "40-50"] = df4050
        df_new = df_new.sort_values(by = ["10-20", "20-30","30-40","40-50"], ascending = [False, False, False, True])
        x = list(df_new.index.get_level_values(0)[:6])
        g1y = list(df_new.loc[x[0]].values[0])
        g2y = list(df_new.loc[x[1]].values[0])
        g3y = list(df_new.loc[x[2]].values[0])
        g4y = list(df_new.loc[x[3]].values[0])

        ind = np.arange(len(g1y))  # the x locations for the groups
        width = 0.2  # the width of the bars

        fig, ax = plt.subplots(figsize=(14, 8))
        rects1 = ax.bar(ind - width/2, g1y, width,
                        color='SkyBlue', label='10-20 años')
        rects2 = ax.bar(ind + width/2, g2y, width,
                        color='IndianRed', label='20-30 años')
        rects3 = ax.bar(ind  + width/2+ width, g3y, width,
                        color='blue', label='30-40 años')

        rects4 = ax.bar(ind  + width/2+ width + width, g4y, width,
                        color='yellow', label='40-50 años')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Edad')
        ax.set_title('Intereses segun la edad')
        ax.set_xticks(ind)
        ax.set_xticklabels(list(df_new.index.get_level_values(0)[:4]))
        ax.legend()


        def autolabel(rects, xpos='center'):
                """
                Attach a text label above each bar in *rects*, displaying its height.

                *xpos* indicates which side to place the text w.r.t. the center of
                the bar. It can be one of the following {'center', 'right', 'left'}.
                """

                xpos = xpos.lower()  # normalize the case of the parameter
                ha = {'center': 'center', 'right': 'left', 'left': 'right'}
                offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

                for rect in rects:
                        height = rect.get_height()
                        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                                '{}'.format(height), ha=ha[xpos], va='bottom')


        autolabel(rects1, "center")
        autolabel(rects2, "center")
        autolabel(rects3, "center")
        autolabel(rects4, "center")

        plt.show()
if __name__ == "__main__":
    data = pd.read_csv("out_blog_data.csv")
    pubvsage = pd.read_csv("out_publications_vs_age.csv")

    # Histograma publicaciones por año

    graficarHistograma(data, "year")

    # Torta de publicaciones por edad
    a = pubvsage[pubvsage["Age"].isin(range(10,15))]
    b =pubvsage[pubvsage["Age"].isin(range(15,20))]
    c = pubvsage[pubvsage["Age"].isin(range(20,25))]
    d = pubvsage[pubvsage["Age"].isin(range(25,30))]
    e = pubvsage[pubvsage["Age"].isin(range(30,40))]
    f = pubvsage[pubvsage["Age"].isin(range(40,50))]

    df = pd.DataFrame({"10-15": [np.sum(a,axis=1).sum()],
                    "15-20": [np.sum(b,axis=1).sum()],
                    "20-25": [np.sum(c,axis=1).sum()],
                    "25-30": [np.sum(d,axis=1).sum()],
                    "30-40": [np.sum(e,axis=1).sum()],
                    "40-50": [np.sum(e,axis=1).sum()],
                    })

    sizes = [df["10-15"][0], df["15-20"][0], df["20-25"][0],
             df["25-30"][0], df["30-40"][0], df["40-50"][0]]
    title = "Publicaciones por edad"
    tags = ["10 - 20 años",
            "15 - 20 años",
            "20 - 25 años",
            "25 - 30 años",
            "30 - 40 años",
            "40 - 50 años"]
    graficarTorta(title, sizes, tags, "Edades")

    # Grafica de intereses segun el genero
    graficarBarchart_gendertopic()
    
    # Grafica publicaciones por genero
    graficarBarchart_agevstopic()