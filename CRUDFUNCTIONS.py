import pyodbc
def create_product(cursor,name,category,price,stock):
    product_name_validation = cursor.execute("SELECT ProductName FROM Products WHERE ProductName = ?",(name,))
    results = product_name_validation.fetchone()
    if results is not None:
        raise ValueError(f"ERROR: Product {results[0]} Already Exists!")
    category_validation = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(category,))
    results = category_validation.fetchone()
    if results is None:
        raise ValueError("ERROR: Category Not Found!")
    else:
        categoryFK = results[0]
    if price <= 0:
        raise ValueError("ERROR: Price Cannot Be Less Than/Equal to 0!")
    if stock <= 0:
        raise ValueError("ERROR: Stock Cannot Be Less Than/Equal to 0!")
    cursor.execute("INSERT INTO Products (ProductName,CategoryFK,ProductPrice,ProductQuantity) VALUES (?,?,?,?)",(name,categoryFK,price,stock))
    return "Product Successfully Created."
    
    

def create_category(cursor,category_name):
    category_validation = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(category_name,))
    fetch = category_validation.fetchone()
    if fetch is not None:
        raise ValueError("ERROR: Category Already Exists!")
    else:
        cursor.execute("INSERT INTO ProductCategory (CategoryName) VALUES (?)",(category_name,))
        return (f"Created Category {category_name}!")

         
def list_products(cursor):
    products = cursor.execute("SELECT * FROM Products")
    fetch = products.fetchall()
    product_list = []
    for item in fetch:
        id,name,categoryFK,price,stock = item
        category = cursor.execute("SELECT CategoryName FROM ProductCategory WHERE CategoryPK = ?",(categoryFK,))
        fetch2 = category.fetchone()
        category_name = fetch2[0]
        product_list.append({"ID":id,"NAME":name,"CATEGORY_NAME":category_name,"CATEGORY_ID":categoryFK,"PRICE":price,"STOCK":stock})
    return product_list

def search_product(cursor,id_or_name):
    try:
        product_id_search = cursor.execute("""
        SELECT ProductCategory.CategoryName,Products.*
        FROM Products
        INNER JOIN ProductCategory
        ON ProductCategory.CategoryPK = Products.CategoryFK
        WHERE ProductPK = ?
        """,(id_or_name,))
    except pyodbc.DataError:
        product_id_search = cursor.execute("""
        SELECT ProductCategory.CategoryName,Products.*
        FROM Products
        INNER JOIN ProductCategory
        ON ProductCategory.CategoryPK = Products.CategoryFK
        WHERE ProductName = ?
        """,(id_or_name,))
    results = product_id_search.fetchone()
    if results is not None:
        category_name,id,name,category_fk,price,stock = results
        return({"ID":id,"NAME":name,"CATEGORY_NAME":category_name,"CATEGORY_ID":category_fk,"PRICE":price,"STOCK":stock})
    else:
        raise ValueError("ERROR: Product Not Found!")
       
        

def update_product(cursor):
    while True:
        try:
            busca = int(input("Digite O ID Do Produto:"))
            if not busca:
                print("ERRO: É Necessário Digitar Um ID!")
                continue
            if busca < 1:
                print("ERRO: ID Inválido, Valor Inicial a partir de 1.")
                continue
            break
        except ValueError:
            print("ERRO: Digite Um Caractere Válido!")
    select1 = cursor.execute("SELECT * FROM Products WHERE ProductPK = ?",(busca,))
    resultado1 = select1.fetchone()
    if resultado1 is None:
        print("ERRO: Produto Não Encontrado!")
        return None
    id,nome,categoriaFK,preco,quantidade = resultado1
    select2 = cursor.execute("SELECT CategoryName FROM ProductCategory WHERE CategoryPK = ?",(categoriaFK,))
    resultado2 = select2.fetchone()
    for item in resultado2:
        nome_categoria = item
    print("Produto Selecionado:")
    print("ID:{}\nNome: {}\nCategoria: {}\nChave Da Categoria: {}\nPreço: R${}\nQuantidade: {} Unidades\n".format(id,nome,nome_categoria,categoriaFK,preco,quantidade))
    print("1 - Nome | 2 - Categoria | 3 - Preço ")
    while True:
        try:
            opcao = int(input("Digite A Opção:"))
            if not opcao:
                print("ERRO: É Necessário Digitar Uma Opção!")
                continue
            if opcao not in [1,2,3]:
                print("ERRO: Digite Uma Opção Válida!")
                continue
            break
        except ValueError:
            print("ERRO: Digite Um Caractere Válido!")
    if opcao == 1:
        while True:
            novo_nome = input("Digite O Novo Nome:")
            novo_nome = novo_nome.lower()
            if not novo_nome:
                print("ERRO: É Necessário Digitar Um Nome!")
                continue
            if novo_nome.isdigit():
                print("ERRO: Nome Não Pode Ser Um Número!")
                continue
            if novo_nome == nome:
                print("ERRO: Novo Nome Não Pode Ser O Nome Atual!")
                continue
            break
        cursor.execute("UPDATE Products SET ProductName = ? WHERE ProductPK = ?",(novo_nome,busca))
        print("Nome Atualizado Com Sucesso!")
    if opcao == 2:
        while True:
            nova_categoria = input("Digite A Nova Categoria:")
            nova_categoria = nova_categoria.lower()
            if not nova_categoria:
                print("ERRO: É Necessário Digitar Uma Categoria!")
                continue
            if nova_categoria.isdigit():
                print("ERRO: Categoria Não Pode Ser Um Número!")
                continue
            if nova_categoria == nome_categoria:
                print("ERRO: Nova Categoria Não Pode Ser A Categoria Atual!")
                continue
            break
        select3 = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(nova_categoria,))
        resultado3 = select3.fetchone()
        for categoriapk in resultado3:
            pass
        if resultado3 is None:
            print("ERRO: Categoria Não Existe!")
            return None
        cursor.execute("UPDATE Products SET CategoryFK = ? WHERE ProductPK = ?",(categoriapk,busca))
        print("Categoria Atualizada Com Sucesso!")
    if opcao == 3:
         while True:
            try:
                novo_preco = float(input("Digite O Novo Preço:"))
                if not novo_preco:
                    print("ERRO: É Necessário Digitar Um Preço!")
                    continue
                if novo_preco <= 0:
                    print("ERRO: Novo Nome Não Pode Ser Menor Ou Igual A Zero!")
                    continue
                if novo_preco == preco:
                    print("ERRO: Novo Preço Não Pode Ser O Mesmo Que O Atual!")
                    continue
                break
            except ValueError:
                print("ERRO: Digite Um Caractere Válido!")
            cursor.execute("UPDATE Products SET ProductPrice = ? WHERE ProductPK = ?",(novo_preco,busca))
            print("Preço Atualizado Com Sucesso!")


def delete_product(cursor,id):
    search = cursor.execute("SELECT * FROM Products WHERE ProductPK = ?",(id,))
    product = search.fetchone()
    if product is None:
        raise ValueError("ERROR: Product Does Not Exist!")
    cursor.execute("DELETE FROM Products WHERE ProductPK = ?",(id,))
    return "Product Successfully Deleted."

