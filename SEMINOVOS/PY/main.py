from PyQt5 import uic,QtWidgets
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape
import locale
import datetime
from datetime import date
import webbrowser


locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')


def abrir_incl():
    inicio.frame.close()
    inicio.frame_2.show()
    inicio.dateEdit.setDate(datetime.date.today())

def fechar_incl():
    inicio.frame.show()
    inicio.frame_2.close()

#incluir veiculos no estoque
def salvar_estq():
    modelo = inicio.lineEdit.text()
    cor = inicio.lineEdit_2.text()
    km = inicio.lineEdit_3.text()
    ano = inicio.lineEdit_4.text()
    placa = inicio.lineEdit_5.text()
    uf = inicio.lineEdit_13.text()
    renavam = inicio.lineEdit_6.text()
    valor = (inicio.lineEdit_7.text().replace(",", "."))
    data = inicio.dateEdit.text()
    responsavel = inicio.lineEdit_9.text()
    contato = inicio.lineEdit_11.text()
    cpf = inicio.lineEdit_12.text()
    pa = inicio.lineEdit_10.text()

    if placa=="":
        inicio.label_18.setText("Itens vazios!")
        inicio.label_17.setText("")
    elif valor=="" :
        inicio.label_18.setText("Itens vazios!")
        inicio.label_17.setText("")
    elif inicio.lineEdit_14.text() == "":
        inicio.label_18.setText("Itens vazios!")
        inicio.label_17.setText("")
    else:
        vp = (inicio.lineEdit_14.text().replace(",", "."))
        try:
            banco = sqlite3.connect('DB/estoque.db')
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS dados (modelo text, cor text, km text, ano text, placa text, uf text, vp text, data date, renavam text, responsavel text, pa text, contato text, cpf text, valor text)")
            cursor.execute("INSERT INTO dados VALUES ('"+modelo+"','"+cor+"','"+km+"','"+ano+"','"+placa+"','"+uf+"','"+vp+"','"+data+"','"+renavam+"','"+responsavel+"','"+pa+"','"+contato+"','"+cpf+"','"+valor+"')")
            banco.commit()
            banco.close()
            inicio.lineEdit.setText("")
            inicio.lineEdit_2.setText("")
            inicio.lineEdit_3.setText("")
            inicio.lineEdit_4.setText("")
            inicio.lineEdit_5.setText("")
            inicio.lineEdit_6.setText("")
            inicio.lineEdit_7.setText("")
            inicio.dateEdit.setDate(datetime.date.today())
            inicio.lineEdit_9.setText("")
            inicio.lineEdit_10.setText("")
            inicio.lineEdit_11.setText("")
            inicio.lineEdit_12.setText("")
            inicio.lineEdit_13.setText("")
            inicio.lineEdit_14.setText("")
            inicio.label_17.setText("Veiculo incluido com sucesso!")
            inicio.label_18.setText("")
        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ",erro)
            erroui.show()

#abrir estoque e detalhes do veiculos
def listar_estq():
    try:
        estoque.show()
        banco = sqlite3.connect('DB/estoque.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dados")
        dados_lidos = cursor.fetchall()
        estoque.tableWidget.setRowCount(len(dados_lidos))

        for i in range (0,len(dados_lidos)):
            for j in range (0,13):
                estoque.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                estoque.tableWidget.setItem(i, 6, QtWidgets.QTableWidgetItem(str(locale.currency((float(dados_lidos[i][6])), grouping=True))))

        banco = sqlite3.connect('DB/estoque.db')
        cursor = banco.cursor()
        sql = f"SELECT SUM(vp) FROM dados"
        cursor.execute(sql)
        sum = cursor.fetchall()
        if str(sum) == "[(None,)]":
            estoque.label_4.setText("R$ 0,00")
        else:
            estoque.label_4.setText((locale.currency(float(sum[0][0]), grouping=True)))

    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ", erro)
        erroui.show()

def detalhes_dados():
    detalhes.show()
    linha = estoque.tableWidget.currentRow()
    try:
        banco = sqlite3.connect('DB/estoque.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dados")
        dados_lidos = cursor.fetchall()
        valor_id = dados_lidos[linha][4]
        cursor.execute("SELECT * FROM dados WHERE placa='"+valor_id+"'")
        edit = cursor.fetchall()


        vlc = str(edit[0][13])
        detalhes.lineEdit.setText(str(edit[0][0]))
        detalhes.lineEdit_2.setText(str(edit[0][1]))
        detalhes.lineEdit_3.setText(str(edit[0][2]))
        detalhes.lineEdit_4.setText(str(edit[0][3]))
        detalhes.lineEdit_5.setText(str(edit[0][4]))
        detalhes.lineEdit_6.setText(str(edit[0][8]))
        detalhes.lineEdit_7.setText(str(edit[0][13]))
        detalhes.lineEdit_8.setText(str(edit[0][7]))
        detalhes.lineEdit_9.setText(str(edit[0][9]))
        detalhes.lineEdit_10.setText(str(edit[0][10]))
        detalhes.lineEdit_11.setText(str(edit[0][11]))
        detalhes.lineEdit_12.setText(str(edit[0][12]))
        detalhes.lineEdit_13.setText(str(edit[0][5]))
        detalhes.lineEdit_7.setText(locale.currency((float(vlc)), grouping=True))

        banco = sqlite3.connect('DB/despesas.db')
        cur = banco.cursor()
        cur.execute("SELECT SUM(valord) FROM dados WHERE plc='" + valor_id + "'")
        edit2 = cur.fetchall()
        ts = str(edit2)
        if ts =="[(None,)]":
            detalhes.lineEdit_14.setText("R$ 0,00")
            detalhes.lineEdit_15.setText(locale.currency((float(vlc)), grouping=True))
        else:
            custo = float(edit2[0][0])
            compra = float(vlc)

            soma = custo+compra
            detalhes.lineEdit_14.setText(locale.currency((float(custo)), grouping=True))
            detalhes.lineEdit_15.setText(locale.currency((float(soma)), grouping=True))

        banco = sqlite3.connect('DB/despesas.db')
        cu = banco.cursor()
        cu.execute("SELECT * FROM dados WHERE plc='"+valor_id+"'")
        edit = cu.fetchall()

        detalhes.tableWidget.setRowCount(len(edit))
        detalhes.tableWidget.setColumnWidth(0, 210)


        for i in range(0, len(edit)):
            for j in range(0, 6):
                detalhes.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(edit[i][j])))
                detalhes.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(locale.currency((float(edit[i][1])), grouping=True))))

    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ", erro)
        erroui.show()

#despesas do carro
def abrir_despesa():
    despesas.show()
    despesas.dateEdit.setDate(datetime.date.today())
    linha = estoque.tableWidget.currentRow()
    try:
        banco = sqlite3.connect('DB/estoque.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dados")
        dados_lidos = cursor.fetchall()
        valor_id = dados_lidos[linha][4]
        cursor.execute("SELECT * FROM dados WHERE placa='" + valor_id + "'")
        edit = cursor.fetchall()

        despesas.lineEdit.setText(str(edit[0][0]))
        despesas.lineEdit_2.setText(str(edit[0][1]))
        despesas.lineEdit_3.setText(str(edit[0][2]))
        despesas.lineEdit_4.setText(str(edit[0][3]))
        despesas.lineEdit_5.setText(str(edit[0][4]))
        despesas.lineEdit_6.setText(str(edit[0][8]))
        despesas.lineEdit_7.setText(locale.currency((float(edit[0][13])), grouping=True))
        despesas.lineEdit_8.setText(str(edit[0][7]))
        despesas.lineEdit_9.setText(str(edit[0][9]))
        despesas.lineEdit_10.setText(str(edit[0][10]))
        despesas.lineEdit_11.setText(str(edit[0][11]))
        despesas.lineEdit_12.setText(str(edit[0][12]))
        despesas.lineEdit_18.setText(str(edit[0][5]))

    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ", erro)
        erroui.show()

def incluir_despesa():
    dp = despesas.lineEdit_13.text()
    valord = (despesas.lineEdit_14.text().replace(",", "."))
    dt = despesas.dateEdit.text()
    rp = despesas.lineEdit_16.text()
    obs = despesas.lineEdit_17.text()
    plc = despesas.lineEdit_5.text()
    if valord=="":
        despesas.label_2.setText("*")
    else:
        try:
            banco = sqlite3.connect('DB/despesas.db')
            cursor = banco.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS dados (dp text, valord int, dt date, rp text, obs text, plc text)")
            cursor.execute(
                "INSERT INTO dados VALUES ('"+dp+"','"+valord+ "','"+dt+"','"+rp+"','"+obs+"','"+plc+"')")
            banco.commit()
            banco.close()

            despesas.lineEdit_13.setText("")
            despesas.lineEdit_14.setText("")
            despesas.dateEdit.setDate(datetime.date.today())
            despesas.lineEdit_16.setText("")
            despesas.lineEdit_17.setText("")


        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ", erro)
            erroui.show()

#vender veiculo
def abrir_venda():
    venda.show()
    venda.dateEdit.setDate(datetime.date.today())
    linha = estoque.tableWidget.currentRow()
    try:
        banco = sqlite3.connect('DB/estoque.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dados")
        dados_lidos = cursor.fetchall()
        valor_id = dados_lidos[linha][4]
        cursor.execute("SELECT * FROM dados WHERE placa='" + valor_id + "'")
        edit = cursor.fetchall()

        venda.lineEdit.setText(str(edit[0][0]))
        venda.lineEdit_2.setText(str(edit[0][1]))
        venda.lineEdit_3.setText(str(edit[0][2]))
        venda.lineEdit_4.setText(str(edit[0][3]))
        venda.lineEdit_5.setText(str(edit[0][4]))
        venda.lineEdit_6.setText(str(edit[0][8]))
        venda.lineEdit_8.setText(str(edit[0][7]))
        venda.lineEdit_9.setText(str(edit[0][9]))
        venda.lineEdit_10.setText(str(edit[0][10]))
        venda.lineEdit_11.setText(str(edit[0][11]))
        venda.lineEdit_12.setText(str(edit[0][12]))
        venda.lineEdit_21.setText(str(edit[0][5]))
        vlc = (str(edit[0][13]))

        banco = sqlite3.connect('DB/despesas.db')
        cur = banco.cursor()
        cur.execute("SELECT SUM(valord) FROM dados WHERE plc='" + valor_id + "'")
        edit2 = cur.fetchall()
        ts = str(edit2)
        if ts == "[(None,)]":
            venda.lineEdit_7.setText(locale.currency((float(vlc)), grouping=True))
            venda.lineEdit_22.setText(str(vlc))
        else:
            custo = float(edit2[0][0])
            compra = float(vlc)
            soma = custo + compra
            venda.lineEdit_7.setText(locale.currency((float(soma)), grouping=True))
            venda.lineEdit_22.setText(str(soma))

    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ", erro)
        erroui.show()


def vender():
    md = venda.lineEdit.text()
    cor = venda.lineEdit_2.text()
    ano = venda.lineEdit_4.text()
    plac = venda.lineEdit_5.text()
    rn = venda.lineEdit_6.text()
    vlr = venda.lineEdit_22.text()
    dte = venda.lineEdit_8.text()
    pa = venda.lineEdit_10.text()
    ct = venda.lineEdit_11.text()
    cpf1 = venda.lineEdit_12.text()
    uf = venda.lineEdit_21.text()
    n = venda.lineEdit_13.text()
    cpf2 = venda.lineEdit_14.text()
    ct2 = venda.lineEdit_15.text()
    email = venda.lineEdit_16.text()
    vl =locale.currency(float(venda.lineEdit_17.text()), grouping=True)
    vv = venda.lineEdit_17.text()
    pg = venda.lineEdit_18.text()
    vendedor = venda.lineEdit_19.text()
    data = datetime.datetime.strptime(venda.dateEdit.text(), "%d/%m/%Y").strftime("%Y-%m-%d")
    lucro = (float(vv))-(float(vlr))
    lc = locale.currency(lucro, grouping=True)

    try:
        banco = sqlite3.connect('DB/relatorio.db')
        cursor = banco.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS dados (md text, cor text, ano text, plac text, uf text, vl text,lc text, data date, vendedor text, rn text, dte date, pa text, ct text, cpf1 text, n text, cpf2 text, ct2 text, email text, pg text, lucro numeric, vlr numeric)")
        cursor.execute(
            "INSERT INTO dados VALUES ('"+md+"','"+cor+"','"+ano+"','"+plac+"','"+uf+"','"+vl+"','"+lc+"','"+data+"','"+vendedor+"','"+rn+"','"+dte+"','"+pa+"','"+ct+"','"+cpf1+"','"+n+"','"+cpf2+"','"+ct2+"','"+email+"','"+pg+"','"+str(lucro)+"','"+vlr+"')")
        banco.commit()
        banco.close()

        venda.lineEdit_13.setText("")
        venda.lineEdit_14.setText("")
        venda.lineEdit_15.setText("")
        venda.lineEdit_16.setText("")
        venda.lineEdit_17.setText("")
        venda.lineEdit_18.setText("")
        venda.lineEdit_19.setText("")

    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ", erro)
        erroui.show()

    seleciona2 = venda.lineEdit_5.text()
    try:
        banco = sqlite3.connect('DB/estoque.db')
        cursor = banco.cursor()
        cursor.execute("DELETE from dados WHERE placa='"+seleciona2+"'")
        banco.commit()
        banco.close()

    except sqlite3.Error as erro:
        print("Erro ao excluir os dados: ", erro)
        erroui.show()

    venda.close()


#abrir relatorio de vendas e detalhes
def relatorio_abrir():
        relatorio.show()
        try:
            banco = sqlite3.connect('DB/relatorio.db')
            cursor = banco.cursor()
            cursor.execute("SELECT * FROM dados")
            dados_lidos = cursor.fetchall()
            relatorio.tableWidget.setRowCount(len(dados_lidos))

            for i in range(0, len(dados_lidos)):
                for j in range(0, 9):
                    relatorio.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                    relatorio.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(datetime.datetime.strptime(str(dados_lidos[i][7]), "%Y-%m-%d").strftime("%d/%m/%Y")))


            banco = sqlite3.connect('DB/relatorio.db')
            cursor = banco.cursor()
            sql = f"SELECT SUM(lucro) FROM dados"
            cursor.execute(sql)
            sum = cursor.fetchall()
            if str(sum) == "[(None,)]":
                relatorio.label_2.setText("R$ 0,00")
            else:
                relatorio.label_2.setText((locale.currency(float(sum[0][0]), grouping=True)))

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ",erro)
            erroui.show()

def abrir_detalhe_vd():
    detalhe_vd.show()
    detalhe_vd.frame.close()
    linha2 = relatorio.tableWidget.currentRow()
    try:
        banco = sqlite3.connect('DB/relatorio.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dados")
        dados_lidos = cursor.fetchall()
        valor_id = dados_lidos[linha2][3]
        cursor.execute("SELECT * FROM dados WHERE plac='"+ valor_id +"'")
        edit = cursor.fetchall()

        detalhe_vd.lineEdit.setText(str(edit[0][0]))
        detalhe_vd.lineEdit_2.setText(str(edit[0][1]))
        detalhe_vd.lineEdit_4.setText(str(edit[0][2]))
        detalhe_vd.lineEdit_5.setText(str(edit[0][3]))
        detalhe_vd.lineEdit_21.setText(str(edit[0][4]))
        detalhe_vd.lineEdit_17.setText(str(edit[0][5]))
        detalhe_vd.lineEdit_7.setText(str(edit[0][6]))
        detalhe_vd.lineEdit_20.setText(datetime.datetime.strptime(str(edit[0][7]), "%Y-%m-%d").strftime("%d/%m/%Y"))
        detalhe_vd.lineEdit_19.setText(str(edit[0][8]))
        detalhe_vd.lineEdit_6.setText(str(edit[0][9]))
        detalhe_vd.lineEdit_8.setText(str(edit[0][10]))
        detalhe_vd.lineEdit_10.setText(str(edit[0][11]))
        detalhe_vd.lineEdit_11.setText(str(edit[0][12]))
        detalhe_vd.lineEdit_12.setText(str(edit[0][13]))
        detalhe_vd.lineEdit_13.setText(str(edit[0][14]))
        detalhe_vd.lineEdit_14.setText(str(edit[0][15]))
        detalhe_vd.lineEdit_15.setText(str(edit[0][16]))
        detalhe_vd.lineEdit_16.setText(str(edit[0][17]))
        detalhe_vd.lineEdit_18.setText(str(edit[0][18]))
        detalhe_vd.lineEdit_3.setText(locale.currency(float(edit[0][20]), grouping=True))
    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ", erro)
        erroui.show()

def custo ():
        detalhe_vd.frame.show()
        valor_id=detalhe_vd.lineEdit_5.text()
        try:
            banco = sqlite3.connect('DB/despesas.db')
            cu = banco.cursor()
            cu.execute("SELECT * FROM dados WHERE plc='" + valor_id + "'")
            edit = cu.fetchall()

            detalhe_vd.tableWidget.setRowCount(len(edit))
            detalhe_vd.tableWidget.setColumnWidth(0, 210)

            for i in range(0, len(edit)):
                for j in range(0, 6):
                    detalhe_vd.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(edit[i][j])))
                    detalhe_vd.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(locale.currency((float(edit[i][1])), grouping=True))))

            bc = banco.cursor()
            bc.execute("SELECT SUM(valord) FROM dados WHERE plc='" + valor_id + "'")
            edit2 = bc.fetchall()
            ts = str(edit2)
            if ts == "[(None,)]":
                detalhe_vd.lineEdit_23.setText("R$ 0,00")
            else:
                detalhe_vd.lineEdit_23.setText((locale.currency(float(edit2[0][0]), grouping=True)))

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ",erro)
            erroui.show()

def fechar_custo():
    detalhe_vd.frame.close()

#filtar o renatorio de vendas por data
def filtro():

    if relatorio.tableWidget.rowCount()>0:
        relatorio.tableWidget.clearContents()

    relatorio.show()
    datainicio = datetime.datetime.strptime(relatorio.dateEdit.text(), "%d/%m/%Y").strftime("%Y-%m-%d")
    datafinal = datetime.datetime.strptime(relatorio.dateEdit_2.text(), "%d/%m/%Y").strftime("%Y-%m-%d")
    try:
        banco = sqlite3.connect('DB/relatorio.db')
        cursor = banco.cursor()
        sql = f"SELECT * FROM dados WHERE data between '{datainicio}' and '{datafinal}'"
        cursor.execute(sql)
        dados_lidos = cursor.fetchall()

        for i in range(0, len(dados_lidos)):
            for j in range(0, 9):
                relatorio.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                relatorio.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(datetime.datetime.strptime(str(dados_lidos[i][7]), "%Y-%m-%d").strftime("%d/%m/%Y")))
        banco = sqlite3.connect('DB/relatorio.db')
        cursor = banco.cursor()
        sql = f"SELECT SUM(lucro) FROM dados WHERE data between '{datainicio}' and '{datafinal}'"
        cursor.execute(sql)
        sum = cursor.fetchall()
        if str(sum)=="[(None,)]":
            relatorio.label_2.setText("R$ 0,00")
        else:
            relatorio.label_2.setText((locale.currency(float(sum[0][0]), grouping=True)))
    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ", erro)
        erroui.show()

#gerar pdf de relatorio de estoque 
def gerar_pdf():
    try:
        banco = sqlite3.connect('DB/estoque.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dados")
        dados_lidos = cursor.fetchall()
        y = 0

        pdf = canvas.Canvas("RELATORIOS/EstoqueSeminovos.pdf", pagesize=landscape(A4))
        pdf.setFont("Helvetica-Bold",16)
        pdf.drawImage('SCR/icn.png',0,560,width=95, height=25)
        pdf.drawString(330,570, "ESTOQUE SEMINOVOS")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(765,575,"QTD")
        pdf.drawString(770,560, str(estoque.tableWidget.rowCount()))
        pdf.setFont("Helvetica-Bold",10)
        pdf.drawString(10,544,"MODELO")
        pdf.drawString(200, 544, "COR")
        pdf.drawString(300, 544, "KM")
        pdf.drawString(370, 544, "ANO/MOD")
        pdf.drawString(450, 544, "PLACA")
        pdf.drawString(530, 544, "UF")
        pdf.drawString(580, 544, "VALOR")
        pdf.drawString(670, 544, "ENTRADA")
        pdf.drawString(750, 544, "RENAVAM")
        pdf.line(5, 555, 830, 555)
        pdf.line(5, 540, 830, 540)


        for i in range(0, len(dados_lidos)):
            pdf.setFont("Helvetica", 10)
            y = y + 15
            pdf.drawString(10,540 - y, str(dados_lidos[i][0]))
            pdf.drawString(200, 540 - y, str(dados_lidos[i][1]))
            pdf.drawString(300, 540 - y, str(dados_lidos[i][2]))
            pdf.drawString(370, 540 - y, str(dados_lidos[i][3]))
            pdf.drawString(450, 540 - y, str(dados_lidos[i][4]))
            pdf.drawString(530, 540 - y, str(dados_lidos[i][5]))
            pdf.drawString(580, 540 - y, str(locale.currency((float(dados_lidos[i][6])), grouping=True)))
            pdf.drawString(670, 540 - y, str(dados_lidos[i][7]))
            pdf.drawString(750, 540 - y, str(dados_lidos[i][8]))
            if (i>1) and (i%49==0):
                pdf.showPage()
                y=0
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawImage('SCR/icn.png', 0, 560, width=95, height=25)
                pdf.drawString(330, 570, "ESTOQUE SEMINOVOS")
                pdf.setFont("Helvetica", 10)
                pdf.drawString(765, 575, "QTD")
                pdf.drawString(770, 560, str(estoque.tableWidget.rowCount()))
                pdf.setFont("Helvetica-Bold", 10)
                pdf.drawString(10, 544, "MODELO")
                pdf.drawString(200, 544, "COR")
                pdf.drawString(300, 544, "KM")
                pdf.drawString(370, 544, "ANO/MOD")
                pdf.drawString(450, 544, "PLACA")
                pdf.drawString(530, 544, "UF")
                pdf.drawString(580, 544, "VALOR")
                pdf.drawString(670, 544, "ENTRADA")
                pdf.drawString(750, 544, "RENAVAM")
                pdf.line(5, 555, 830, 555)
                pdf.line(5, 540, 830, 540)
        pdf.save()

        webbrowser.open("RELATORIOS/EstoqueSeminovos.pdf")

    except sqlite3.Error as erro:
        print("Erro ao editar os dados: ",erro)
        erroui.show()

#gerar pdf de relatorios de vendas
def gerar_pdf2():
    try:
        datainicio = datetime.datetime.strptime(relatorio.dateEdit.text(), "%d/%m/%Y").strftime("%Y-%m-%d")
        datafinal = datetime.datetime.strptime(relatorio.dateEdit_2.text(), "%d/%m/%Y").strftime("%Y-%m-%d")
        banco = sqlite3.connect('DB/relatorio.db')
        cursor = banco.cursor()
        sql = f"SELECT * FROM dados WHERE data between '{datainicio}' and '{datafinal}'"
        cursor.execute(sql)
        dados_lidos = cursor.fetchall()
        periodo = relatorio.dateEdit.text() + " até " + relatorio.dateEdit_2.text()

        if str(dados_lidos) == "[]":
            banco = sqlite3.connect('DB/relatorio.db')
            cursor = banco.cursor()
            cursor.execute("SELECT * FROM dados")
            dados_lidos = cursor.fetchall()

            periodo = "2021-01-01 até " + str(date.today())
        y = 0

        pdf = canvas.Canvas("RELATORIOS/RelatorioSeminovos.pdf", pagesize=landscape(A4))
        pdf.setFont("Helvetica-Bold",16)
        pdf.drawImage('SCR/icn.png', 0, 560, width=95, height=25)
        pdf.drawString(280,570, "RELATÓRIO DE VENDAS SEMINOVOS")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(765,575,"QTD")
        pdf.drawString(770,560, str(relatorio.tableWidget.rowCount()))
        pdf.setFont("Helvetica-Bold",10)
        pdf.drawString(10, 544, "DATA")
        pdf.drawString(90,544,"MODELO")
        pdf.drawString(260, 544, "COR")
        pdf.drawString(350, 544, "ANO/MOD")
        pdf.drawString(420, 544, "PLACA")
        pdf.drawString(490, 544, "UF")
        pdf.drawString(530, 544, "VALOR")
        pdf.drawString(630, 544, "LUCRO")
        pdf.drawString(730, 544, "VENDEDOR")
        pdf.line(5,555,830,555)
        pdf.line(5,540, 830,540)


        for i in range(0, len(dados_lidos)):
            pdf.setFont("Helvetica", 10)
            y = y + 15
            pdf.drawString(10,540 - y, str(datetime.datetime.strptime(dados_lidos[i][7], "%Y-%m-%d").strftime("%d/%m/%Y")))
            pdf.drawString(90, 540 - y, str(dados_lidos[i][0]))
            pdf.drawString(260, 540 - y, str(dados_lidos[i][1]))
            pdf.drawString(350, 540 - y, str(dados_lidos[i][2]))
            pdf.drawString(420, 540 - y, str(dados_lidos[i][3]))
            pdf.drawString(490, 540 - y, str(dados_lidos[i][4]))
            pdf.drawString(530, 540 - y, str(dados_lidos[i][5]))
            pdf.drawString(630, 540 - y, str(dados_lidos[i][6]))
            pdf.drawString(730, 540 - y, str(dados_lidos[i][8]))

            if (i>1) and (i%30==0):
                pdf.showPage()
                y=0
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawImage('SCR/icn.png', 0, 560, width=95, height=25)
                pdf.drawString(280, 570, "RELATÓRIO DE VENDAS SEMINOVOS")
                pdf.setFont("Helvetica", 10)
                pdf.drawString(765, 575, "QTD")
                pdf.drawString(770, 560, str(relatorio.tableWidget.rowCount()))
                pdf.setFont("Helvetica-Bold", 10)
                pdf.drawString(10, 544, "DATA")
                pdf.drawString(90, 544, "MODELO")
                pdf.drawString(260, 544, "COR")
                pdf.drawString(350, 544, "ANO/MOD")
                pdf.drawString(420, 544, "PLACA")
                pdf.drawString(490, 544, "UF")
                pdf.drawString(530, 544, "VALOR")
                pdf.drawString(630, 544, "LUCRO")
                pdf.drawString(730, 544, "VENDEDOR")
                pdf.line(5, 555, 830, 555)
                pdf.line(5, 540, 830, 540)

        pdf.line(5, 40, 830, 40)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(690, 15, "LUCRO:"+str(relatorio.label_2.text()))
        pdf.drawString(15, 15, "PERIODO:"+str(periodo))
        pdf.save()

        webbrowser.open("RELATORIOS/RelatorioSeminovos.pdf")

    except sqlite3.Error as erro:
        print("Erro ao editar os dados: ",erro)
        erroui.show()

#converter QT em python
app=QtWidgets.QApplication([])
inicio = uic.loadUi("QT/inicio.ui")
despesas = uic.loadUi("QT/despesa.ui")
detalhes = uic.loadUi("QT/detalhes.ui")
estoque = uic.loadUi("QT/estoque.ui")
relatorio = uic.loadUi("QT/relatorio.ui")
venda = uic.loadUi("QT/venda.ui")
detalhe_vd = uic.loadUi("QT/detalhe_vd.ui")
erroui = uic.loadUi("QT/erro.ui")

#conexão com botões
inicio.incluir.clicked.connect(abrir_incl)
inicio.incl.clicked.connect(salvar_estq)
inicio.pushButton.clicked.connect(fechar_incl)
inicio.estoque.clicked.connect(listar_estq)
estoque.atualizar.clicked.connect(listar_estq)
inicio.relatorio.clicked.connect(relatorio_abrir)
estoque.detalhe.clicked.connect(detalhes_dados)
estoque.incl_d.clicked.connect(abrir_despesa)
estoque.vd.clicked.connect(abrir_venda)
venda.incld.clicked.connect(vender)
despesas.incld.clicked.connect(incluir_despesa)
relatorio.detalhe.clicked.connect(abrir_detalhe_vd)
detalhe_vd.pushButton_2.clicked.connect(custo)
detalhe_vd.pushButton.clicked.connect(fechar_custo)
relatorio.filtro_2.clicked.connect(filtro)
relatorio.limpar.clicked.connect(relatorio_abrir)
estoque.excel.clicked.connect(gerar_pdf)
relatorio.imp.clicked.connect(gerar_pdf2)

#inicialização do programa
inicio.show()
app.exec()
