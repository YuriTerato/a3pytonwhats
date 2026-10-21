import os
import re
import pandas as pd
import matplotlib.pyplot as plt


def ler_conversa(caminho):
    linhas = []

    with open(caminho, encoding='utf-8') as arquivo:
        for linha in arquivo:
            # mensagens do sistema e anexos vem com um caractere invisivel, ignora
            if '\u200e' in linha:
                continue

            # formato: [20/10/2026, 23:28:44] Nome: mensagem
            resultado = re.match(r'\[(\d+/\d+/\d+),? (\d+:\d+):\d+\] (.*?): (.*)', linha)
            if resultado:
                linhas.append(resultado.groups())

    df = pd.DataFrame(linhas, columns=['data', 'hora', 'remetente', 'mensagem'])
    df['data'] = pd.to_datetime(df['data'], dayfirst=True).dt.date
    return df


def pedir_remetente(df):
    print('Remetentes:', ', '.join(df['remetente'].unique()))
    nome = input('Digite o nome do remetente: ')

    if nome not in df['remetente'].values:
        print('Remetente nao encontrado.')
        return None
    return nome


def main():
    caminho = input('Caminho do arquivo da conversa (.txt): ').strip('"')

    if not os.path.isfile(caminho):
        print('Arquivo nao encontrado.')
        return

    df = ler_conversa(caminho)
    print(df.to_string())

    while True:
        print()
        print('1 - Resumo das conversas')
        print('2 - Historico do remetente')
        print('3 - Grafico do historico do remetente')
        print('4 - Grafico de pizza')
        print('5 - Grafico de linhas')
        print('0 - Sair')
        opcao = input('Escolha uma opcao: ')

        if opcao == '1':
            print(df['remetente'].value_counts())

        elif opcao == '2':
            nome = pedir_remetente(df)
            if nome:
                print(df[df['remetente'] == nome][['data', 'hora', 'mensagem']].to_string())

        elif opcao == '3':
            nome = pedir_remetente(df)
            if nome:
                df[df['remetente'] == nome].groupby('data').size().plot(kind='bar')
                plt.title('Mensagens por dia, ' + nome)
                plt.xlabel('Data')
                plt.ylabel('Quantidade')
                plt.tight_layout()
                plt.show()

        elif opcao == '4':
            df['remetente'].value_counts().plot(kind='pie', autopct='%1.1f%%')
            plt.title('Percentual de mensagens por remetente')
            plt.ylabel('')
            plt.show()

        elif opcao == '5':
            df.groupby(['data', 'remetente']).size().unstack(fill_value=0).plot(kind='line', marker='o')
            plt.title('Mensagens ao longo do tempo')
            plt.xlabel('Data')
            plt.ylabel('Quantidade')
            plt.tight_layout()
            plt.show()

        elif opcao == '0':
            break

        else:
            print('Opcao invalida.')


main()
