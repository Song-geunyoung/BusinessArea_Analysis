import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

Sales_csv = pd.read_csv("Sales.csv", encoding='cp949', low_memory=False)
LivingPopulation_csv = pd.read_csv("LivingPopulation.csv", encoding='cp949', low_memory=False)
WorkerPopulation_csv = pd.read_csv("WorkerPopulation.csv", encoding='cp949', low_memory=False)
ResidentPopulation_csv = pd.read_csv("ResidentPopulation.csv", encoding='cp949', low_memory=False)
SimilarBusiness_csv = pd.read_csv("SimilarBusiness.csv", encoding='cp949', low_memory=False)
Attraction_csv = pd.read_csv("Attraction.csv", encoding='cp949', low_memory=False)
Income_csv = pd.read_csv("Income.csv", encoding='cp949', low_memory=False)

"""
#NodeList 인자
0기준년도       1기준분기       2상권구분코드   3상권종류   4상권코드   5상권코드명
6서비스업코드   7서비스업명     8분기당매출     9생활인구   10직장인구  11거주인구
12유사업종 수   13집객시설 수   14월소득
"""

#함수----------------------------------------------------------------------------------------------

#NodeList에 매출(Sales) 추가
def Append_Sales(Receive_List, BusinessType):
    SalesList = Sales_csv.values.tolist()
    for i in range(len(SalesList)):
        if(SalesList[i][7] == BusinessType):
            Receive_List.append(SalesList[i][:9])

#매출을 0~1 사이로 가중치화
def Weighting(Receive_List):
    max = Receive_List[0][8]
    for i in range(len(Receive_List)):
        if(max < Receive_List[i][8]):
            max = Receive_List[i][8]
    for i in range(len(Receive_List)):
        Receive_List[i][8] = Receive_List[i][8]/(max+1)

#NodeList에 csv데이터 추가
def Append_csvtoList(csvData, NodeList, Receive_List, RefNum):
    Receive_List = csvData.values.tolist()
    for i in range (len(NodeList)):
        for j in range(len(Receive_List)):
            if(NodeList[i][4] == Receive_List[j][4]):#상권코드가 같으면
                NodeList[i].append(Receive_List[j][RefNum])
                break

#기준Edge 20분할로 나누어 추가
def Add_Edge(Receive_List, num, BusinessType):
    max = min = Receive_List[0][num]
    for i in range(len(Receive_List)):
        if(max < Receive_List[i][num]):
            max = Receive_List[i][num]
        if(min > Receive_List[i][num]):
            min = Receive_List[i][num]

    if(num==9):
        NodeName = "유동인구"
    elif(num==10):
        NodeName = "직장인구"
    elif(num==11):
        NodeName = "거주인구"
    elif(num==12):
        NodeName = "유사업종 수"
    elif(num==13):
        NodeName = "집객시설 수"
    elif(num==14):
        NodeName = "월소득"

    #추가 가중치 조절 부분
    for i in range(len(Receive_List)):
        for j in range(0,20):
            if( min+(max-min)/20*(j) <= Receive_List[i][num] and Receive_List[i][num] <= min+(max-min)/20*(j+1) and num != 12):
                    if(num==9):
                        GraphResult.add_edge(Receive_List[i][5] + " " + BusinessType, NodeName + str(j+1), weight = 1-Receive_List[i][8]*0.166 )
                    elif(num==10):
                        GraphResult.add_edge(Receive_List[i][5] + " " + BusinessType, NodeName + str(j+1), weight = 1-Receive_List[i][8]*0.166)
                    elif(num==11):
                        GraphResult.add_edge(Receive_List[i][5] + " " + BusinessType, NodeName + str(j+1), weight = 1-Receive_List[i][8]*0.166)
                    elif(num==13):
                        GraphResult.add_edge(Receive_List[i][5] + " " + BusinessType, NodeName + str(j+1), weight = 1-Receive_List[i][8]*0.166 )
                    elif(num==14):
                        GraphResult.add_edge(Receive_List[i][5] + " " + BusinessType, NodeName + str(j+1), weight = 1-Receive_List[i][8]*0.166 )

            elif( min+(max-min)/20*(j) <= Receive_List[i][num] and Receive_List[i][num] <= min+(max-min)/20*(j+1) and num == 12):
                GraphResult.add_edge(Receive_List[i][5] + " " + BusinessType, NodeName + str(j+1), weight = Receive_List[i][8]*0.166 )

#메인----------------------------------------------------------------------------------------------

NodeList = SalesList = LivingList = WorkerList = ResidentList = SimilarList  = AttractionList = IncomeList = list()

print("업종을 입력해주세요 : ")
BusinessType = input()

Append_Sales(NodeList, BusinessType)
Weighting(NodeList)
Append_csvtoList(LivingPopulation_csv, NodeList, LivingList, 6)
Append_csvtoList(WorkerPopulation_csv, NodeList, WorkerList, 6)
Append_csvtoList(ResidentPopulation_csv, NodeList, ResidentList, 6)
Append_csvtoList(SimilarBusiness_csv, NodeList, SimilarList, 9)
Append_csvtoList(Attraction_csv, NodeList, AttractionList, 6)
Append_csvtoList(Income_csv, NodeList, AttractionList, 6)

print(NodeList)

#그래프 생성----------------------------------------------------------------------------------------
GraphResult = nx.Graph()
#행정동 노드 추가
for i in range(len(NodeList)):
    GraphResult.add_node(NodeList[i][5] + " " + BusinessType)

#상주인구, 직장인구 노드 추가
for i in range(0,20):
    GraphResult.add_node("유동인구" + str(i+1))
    GraphResult.add_node("직장인구" + str(i+1))
    GraphResult.add_node("거주인구" + str(i+1))
    GraphResult.add_node("유사업종 수" + str(i+1))
    GraphResult.add_node("집객시설 수" + str(i+1))
    GraphResult.add_node("월소득" + str(i+1))

#LivingPopulation, WorkerPopulation, ResidentPopulation, SimilarBusiness, Attraction, Income 순 엣지 추가
for i in range(9,15):
    Add_Edge(NodeList, i, BusinessType)

#그래프 형성
nx.write_gexf(GraphResult, "BusinessArea_Analysis_WeightedDegree.gexf")