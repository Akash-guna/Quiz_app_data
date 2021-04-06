from flask import Flask,jsonify
import os
import random
import pandas as pd

app=Flask(__name__)
def conv_dict(data):
    ret_data=[]
    for row in data:
        dict={}
        s= str(row[0].encode("ascii", errors="replace"))[2:-2]
        dict["question"]=s
        dict_opts={}
        print(row[1])
        for i in range(int(row[1])):
            dict_opts["Option"+str(i+1)]=row[2][i]
            if row[2][i]== row[3]:
                dict["correct_opt"]= i+1
        dict["options"]=dict_opts
        ret_data.append(dict)
    return ret_data
def conv_dict_map(data,areas):
    ret_data=[]
    area_details=pd.read_json("areas.json")

    ad_np=area_details.to_numpy()
    lat=None
    long=None
    for i in range(len(areas)):
        for j in range(ad_np.shape[0]):

            if ad_np[j][0]==areas[i]:
                lat=ad_np[j][1]
                long=ad_np[j][2]
                print(lat,long)
        loc_array=[]
        for j in range(len(data[i])):
            d={"Name":data[i][j][0],"Latitude":data[i][j][1],"Longitude":data[i][j][2]}
            loc_array.append(d)
        fin_dict={"Area_Name":areas[i],"Latitude":lat,"Longitude":long,"No_Loc":len(loc_array),"Locations":loc_array}
        ret_data.append(fin_dict)
    return ret_data

@app.route("/get_questions", methods=["GET","POST"])
def questions():
    database=pd.read_json("quiz_questions.json")
    #del database[database.keys()[0]]
    data=database.to_numpy()
    rand_ids=random.sample(range(0,len(data)-1),140)
    rand_rows_big=[data[i] for i in rand_ids[:130]]
    rand_rows_small=[data[i] for i in rand_ids[130:]]
    big_row_dict_conv=conv_dict(rand_rows_big)
    small_row_dict_conv=conv_dict(rand_rows_small)
    question_dict={"Big_Pool":big_row_dict_conv,"Small_Pool":small_row_dict_conv}
    return jsonify(question_dict)
@app.route("/map_questions",methods=["GET","POST"])
def map_json():
    db=pd.read_json("location.json")
    data=db.to_numpy()
    areas=db["Area"].unique()
    rand_ids=random.sample(range(0,areas.shape[0]-1),20)
    output_data_big=[]
    for r in rand_ids[:15]:
        loc_area_big=[]
        for row in data:
            if areas[r] == row[1]:
                loc_area_big.append([row[0],row[3],row[4]])
        r_idx=random.sample(range(0,min(5,len(loc_area_big)-1)),min(5,len(loc_area_big)-1))
        output_data_big.append([loc_area_big[i] for i in r_idx])
    converted_big_out=conv_dict_map(output_data_big,[areas[i] for i in rand_ids[:15]])
    output_data_small=[]
    for r in rand_ids[15:]:
        loc_area_small=[]
        for row in data:
            if areas[r] == row[1]:
                loc_area_small.append([row[0],row[3],row[4]])
        r_idx=random.sample(range(0,min(5,len(loc_area_small)-1)),min(5,len(loc_area_small)-1))
        output_data_small.append([loc_area_small[i] for i in r_idx])
    converted_small_out=conv_dict_map(output_data_small,[areas[i] for i in rand_ids[15:]])
    out_dict={"Big_Pool":converted_big_out,"Small_Pool":converted_small_out}
    return jsonify(out_dict)
@app.route("/imgs_data",methods=["GET","POST"])
def imgs():
    data=pd.read_csv("col_data.csv")
    del data[data.keys()[0]]
    np_data=data.to_numpy()
    r=random.sample(range(0,np_data.shape[0]),175)
    s_tuples=[np_data[ra] for ra in r]
    conv_big_pool=[]
    for i in s_tuples[:150]:
        dict={"Image_Name":i[0],"Blue":i[1],"Green":i[2],"Yellow":i[3],"Red":i[4],"Violet":i[5]}
        conv_big_pool.append(dict)
    conv_small_pool=[]
    for i in s_tuples[150:]:
        dict={"Image_Name":i[0],"Blue":i[1],"Green":i[2],"Yellow":i[3],"Red":i[4],"Violet":i[5]}
        conv_small_pool.append(dict)
    out_dict={"Big_Pool":conv_big_pool,"Small_Pool":conv_small_pool}
    return out_dict
@app.route("/imgs_data_arr",methods=["GET","POST"])
def imgs_arr():
    data=pd.read_csv("col_data.csv")
    del data[data.keys()[0]]
    np_data=data.to_numpy()
    r=random.sample(range(0,np_data.shape[0]),175)
    s_tuples=[np_data[ra] for ra in r]
    conv_big_pool=[]
    for i in s_tuples[:150]:
        dict={"Image_Name":i[0],"Colour_Present":[i[1],i[2],i[3],i[4],i[5]]}
        conv_big_pool.append(dict)
    conv_small_pool=[]
    for i in s_tuples[150:]:
        dict={"Image_Name":i[0],"Colour_Present":[i[1],i[2],i[3],i[4],i[5]]}
        conv_small_pool.append(dict)
    out_dict={"Big_Pool":conv_big_pool,"Small_Pool":conv_small_pool}
    return out_dict
if __name__ == "__main__":
    app.run(debug=True)
