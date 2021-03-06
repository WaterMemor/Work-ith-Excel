@app.route('/code')
def code():
   db = pymysql.connect("localhost", login, password, dataBase)
   cursor =db.cursor() 
   cursor.execute("SELECT * from orders")
   data = cursor.fetchall()
 #return render_template('index.html', results=data)
   #print(data)
   output = BytesIO()
   writer = pd.ExcelWriter(output, engine='xlsxwriter')
   workbook = writer.book
   bold = workbook.add_format({'bold': True, 'font_size':11,'border':1,'text_wrap':1,'align':'center'})
   bordered = workbook.add_format({'border':1,'text_wrap':1,'align':'center'})
   #bold.set_border(1)
   align_center = workbook.add_format({'align': 'center','border':1})
   align_right = workbook.add_format({'align': 'right'})
   worksheet = workbook.add_worksheet()
   worksheet.set_column(0, 10, 15)  
   worksheet.write('A1', 'Отчет',bold)
   
   worksheet.write('A6', 'id ордера',bold)
   worksheet.write('B6', 'id цикла',bold)
   worksheet.write('C6', 'Биржа',bold)
   worksheet.write('D6', 'Пара',bold)
   worksheet.write('E6', 'Статус',bold)
   worksheet.write('F6', 'Тип',bold)
   worksheet.write('G6', 'Количество',bold)
   worksheet.write('H6', 'Цена',bold)
   worksheet.write('I6', 'Объем / Стратегия',bold)
   worksheet.write('J6', 'Переход',bold)
   worksheet.write('K6', 'Начало / конец / продолжительность',bold)

   
   i=7
   for key in data:
      worksheet.write('A'+str(i), key[1],bordered)
      worksheet.write('B'+str(i), key[2],bordered)
      worksheet.write('C'+str(i), key[7],bordered)
      worksheet.write('D'+str(i), key[8],bordered)
      worksheet.write('E'+str(i), key[10],bordered)
      worksheet.write('F'+str(i), key[11],bordered)
      worksheet.write('G'+str(i), key[14],bordered)
      worksheet.write('H'+str(i), key[13],bordered)
      worksheet.write('I'+str(i), key[6],bordered)

      l1='url'+key[8]
    
      worksheet.write_url('J'+str(i), l1, bordered, string='продолжить')
     
      worksheet.write('K'+str(i), 'Начало: '+str(key[3])+'/Конец:'+str(key[4])+'/продолжительность',bordered)
      i=i+1
   
   writer.close()
   output.seek(0)
   cursor.close()
   db.close()
   return send_file(output, attachment_filename="Отчет.xlsx", as_attachment=True)
