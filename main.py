import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

Sales_csv = pd.read_csv("Sales.csv", encoding='cp949', low_memory=False)
LivingPopulation_csv = pd.read_csv("LivingPopulation.csv", encoding='cp949', low_memory=False)
Income_csv = pd.read_csv("Income.csv", encoding='cp949', low_memory=False)
WorkerPopulation_csv = pd.read_csv("WorkerPopulation.csv", encoding='cp949', low_memory=False)

"""
#NodeList
0기준년도       1기준분기       2상권구분코드   3상권종류   4상권코드   5상권코드명
6서비스업코드   7서비스업명     8분기당매출     9거주인구   10직장인구  11월평균수입
"""

#함수----------------------------------------------------------------------------------------------

#NodeList에 매출(Sales) 추가
def Append_Sales(Receive_List, BusinessType):
    SalesList = Sales_csv.values.tolist()
    for i in range(len(SalesList)):
        if(SalesList[i][7] == BusinessType):
            Receive_List.append(SalesList[i][:9])

#매출을 0~1 사이로 가중치화
def weighting(Receive_List):
    max = Receive_List[0][8]
    for i in range(len(Receive_List)):
        if(max < Receive_List[i][8]):
            max = Receive_List[i][8]
    for i in range(len(Receive_List)):
        Receive_List[i][8] = Receive_List[i][8]/max

#NodeList에 csv데이터 추가
def Append_csvtoList(csvData, NodeList, Receive_List):
    Receive_List = csvData.values.tolist()
    for i in range (len(NodeList)):
        for j in range(len(Receive_List)):
            if(NodeList[i][4] == Receive_List[j][4]):#상권코드가 같으면
                NodeList[i].append(Receive_List[j][6])
                break

#인구Edge 20분할로 나누어 추가
def Add_Edge_Population(Receive_List, num, BusinessType):
    max = min = Receive_List[0][num]
    for i in range(len(Receive_List)):
        if(max < Receive_List[i][num]):
            max = Receive_List[i][num]
        if(min > Receive_List[i][num]):
            min = Receive_List[i][num]

    if(num==9):
        NodeName = "LivingPopulation"
    elif(num==10):
        NodeName = "WorkerPopulation"

    for i in range(len(Receive_List)):
        for j in range(0,20):
            if( min+(max-min)/20*(j) <= Receive_List[i][num] and Receive_List[i][num] <= min+(max-min)/20*(j+1) ):
                GraphResult.add_edge(Receive_List[i][5] + " " + BusinessType, NodeName + str(j+1), weight = Receive_List[i][8])            

#메인----------------------------------------------------------------------------------------------

NodeList = SalesList = LivingList = WorkerList = IncomeList = []

print("업종을 입력해주세요 : ")
BusinessType = input()

Append_Sales(NodeList, BusinessType)
weighting(NodeList)
Append_csvtoList(LivingPopulation_csv, NodeList, LivingList)
Append_csvtoList(WorkerPopulation_csv, NodeList, WorkerList)
# Append_csvtoList(Income_csv, NodeList, IncomeList)

#그래프 생성----------------------------------------------------------------------------------------

GraphResult = nx.Graph()
#행정동 노드 추가
for i in range(len(NodeList)):
    GraphResult.add_node(NodeList[i][5] + " " + BusinessType)

#거주인구, 직장인구 노드 추가
for i in range(0,20):
    GraphResult.add_node("LivingPopulation" + str(i+1))
    GraphResult.add_node("WorkerPopulation" + str(i+1))

Add_Edge_Population(NodeList, 9, BusinessType)
Add_Edge_Population(NodeList, 10, BusinessType)

#그래프 형성
nx.write_gexf(GraphResult, "TradeArea_Analysis.gexf")