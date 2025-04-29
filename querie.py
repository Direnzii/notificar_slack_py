def alerta_pedidos_combo():
    return f"""SELECT DISTINCT p.id, c.id, c.TITULO, u.usuario, cli.CNPJ, cli.NOMEFANTASIA, f.cnpj, 
                f.NOMEFANTASIA, ct.nome, p.dataenvio, p.situacao FROM pedido p
                    INNER JOIN RESPOSTACLIENTE rc ON rc.IDCOTACAO = p.IDCOTACAO
                    INNER JOIN RESPOSTACLIENTEITEM rci ON rci.IDRESPOSTACLIENTE = rc.id
                    INNER JOIN PEDIDOMANUALITEMRESPOSTA pmir ON pmir.IDRESPOSTACLIENTEITEM = rci.id
                    inner join cliente cli on cli.id = p.idcliente
                    inner join conta cont on cont.id = p.IDCOMPRADOR
                    inner join usuario u on u.id = cont.idusuario
                    INNER JOIN COTACAO c ON c.id = p.IDCOTACAO
                    INNER JOIN FORNECEDOR f ON f.id = p.IDFORNECEDOR
                    INNER JOIN conta c2 ON c2.id = p.IDREPRESENTANTE
                    INNER JOIN contato ct ON ct.ID = c2.IDCONTATO
                    inner join pedidoitem pi on pi.idproduto = pmir.idproduto and pi.idpedido = p.id
                    WHERE trunc(p.DATAENVIO) = TRUNC(SYSDATE)
                    AND rc.COMBO = 1
                    AND pmir.COMBO = 1
                    AND pmir.COMPRARCLIENTE = 1
                    AND p.situacao >= 3
                    ORDER BY p.dataenvio DESC
                    FETCH FIRST 1 ROWS ONLY"""