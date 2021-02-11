def to_buy(*new_items, shopping_list = []): #тут скорее всего на вход три позиционных
    for i in new_items:
        shopping_list.append(i) # новый список не был создан потому, что мы все аппендим в один список. 
    return shopping_list

monday = to_buy('яблоки', 'молоко', 'хлеб')
print(monday)

tuesday = to_buy('груши', 'йогурт', 'мясо')
print(tuesday)