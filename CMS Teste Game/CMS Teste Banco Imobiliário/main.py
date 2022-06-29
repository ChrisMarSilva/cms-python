from typing import List
import random


class Propriedade(object):

    def __init__(self, sequencia: int, vlr_venda: float, vlr_aluguel: float):
        self.sequencia: int = sequencia
        self.vlr_venda: float = vlr_venda
        self.vlr_aluguel: float = vlr_aluguel
        self.proprietario: Jogador = None

    def __repr__(self):
        return f'Propriedade (Sequencia: {self.sequencia} - Vlr. Venda: {self.vlr_venda:.2f}- Vlr. Aluguel: {self.vlr_aluguel:.2f}- Proprietario: {self.proprietario:})'


class Jogador(object):
    
    def __init__(self, numero: int, nome: str, saldo: float, posicao: int, vitorias: int):
        self.numero: int = numero
        self.nome: str = nome
        self.saldo: float = saldo
        self.posicao: int = posicao
        self.vitorias: int = vitorias

    def JogarDado(self, tabuleiro: List[Propriedade]) -> None:

        random.seed()
        numero_dado = random.randint(1, 6)
        self.posicao += numero_dado
        if self.posicao > 20:
            self.posicao -= 20

        propriedade = tabuleiro[self.posicao-1]
        if propriedade.proprietario == None:
            if self.DecideCompra(vlr_venda=propriedade.vlr_venda, vlr_aluguel=propriedade.vlr_aluguel):
                self.saldo -= propriedade.vlr_venda
                if self.saldo > 0.0:
                    propriedade.proprietario = self
                else:
                    for p in tabuleiro:
                        if p.proprietario is not None and p.proprietario.numero == self.numero:
                            p.proprietario = None
        else:
            self.saldo -= propriedade.vlr_aluguel
            propriedade.proprietario.saldo += propriedade.vlr_aluguel

    def DecideCompra(self, vlr_venda: float, vlr_aluguel: float) -> bool:
        if self.numero == 1:  # impulsivo
            return True
        if self.numero == 2 and vlr_aluguel > 50.0:  # exigente
            return True
        if self.numero == 3 and self.saldo - vlr_venda >= 80.0:  # cauteloso
            return True
        if self.numero == 4 and random.random() >= .5:  # aleatório
            return True
        return False

    def __repr__(self):
        return f'Jogador (Numero: {self.numero} - Nome: {self.nome} - Saldo: {self.saldo:.2f} - Posição Atual: {self.posicao})'


def IniciarJogo(tabuleiro: List[Propriedade], jogadores: List[Jogador]) -> None:

    random.seed()
    numero_jogar = random.randint(0, len(jogadores) - 1)
    jogador = jogadores[numero_jogar]

    numero_voltas = 1
    while True:

        jogador.JogarDado(tabuleiro=tabuleiro)

        if jogador.saldo <= 0.0:
            jogadores.pop(numero_jogar)
            numero_jogar -= 1

        if len(jogadores) == 1:
            break

        numero_jogar += 1
        if numero_jogar >= len(jogadores):
            numero_jogar = 0
            numero_voltas += 1
            for j in jogadores:
                j.saldo += 100.00

        if numero_voltas > 1000:
            break

        jogador = jogadores[numero_jogar]

    vencedores = sorted(jogadores, key=lambda x: x.saldo, reverse=True)
    timeout = numero_voltas > 1000
    return timeout, numero_voltas, vencedores


def main():

    p01 = Propriedade(sequencia=1, vlr_venda=100.0, vlr_aluguel= 100.0)
    p02 = Propriedade(sequencia=2, vlr_venda=200.0, vlr_aluguel= 200.0)
    p03 = Propriedade(sequencia=3, vlr_venda=300.0, vlr_aluguel= 100.0)
    p04 = Propriedade(sequencia=4, vlr_venda=400.0, vlr_aluguel= 200.0)
    p05 = Propriedade(sequencia=5, vlr_venda=500.0, vlr_aluguel= 100.0)
    p06 = Propriedade(sequencia=6, vlr_venda=600.0, vlr_aluguel= 200.0)
    p07 = Propriedade(sequencia=7, vlr_venda=700.0, vlr_aluguel= 100.0)
    p08 = Propriedade(sequencia=8, vlr_venda=800.0, vlr_aluguel= 200.0)
    p09 = Propriedade(sequencia=9, vlr_venda=900.0, vlr_aluguel= 100.0)
    p10 = Propriedade(sequencia=10, vlr_venda=1000.0, vlr_aluguel= 200.0)
    p11 = Propriedade(sequencia=11, vlr_venda=1100.0, vlr_aluguel= 100.0)
    p12 = Propriedade(sequencia=12, vlr_venda=1200.0, vlr_aluguel= 200.0)
    p13 = Propriedade(sequencia=13, vlr_venda=1300.0, vlr_aluguel= 100.0)
    p14 = Propriedade(sequencia=14, vlr_venda=1400.0, vlr_aluguel= 200.0)
    p15 = Propriedade(sequencia=15, vlr_venda=1500.0, vlr_aluguel= 100.0)
    p16 = Propriedade(sequencia=16, vlr_venda=1600.0, vlr_aluguel= 200.0)
    p17 = Propriedade(sequencia=17, vlr_venda=1700.0, vlr_aluguel= 100.0)
    p18 = Propriedade(sequencia=18, vlr_venda=1800.0, vlr_aluguel= 200.0)
    p19 = Propriedade(sequencia=19, vlr_venda=1900.0, vlr_aluguel= 100.0)
    p20 = Propriedade(sequencia=20, vlr_venda=2000.0, vlr_aluguel= 200.0)
    tabuleiro = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20]

    j1 = Jogador(numero=1, nome='Impulsivo', saldo=3000.0, posicao=0, vitorias=0)
    j2 = Jogador(numero=2, nome='Exigente', saldo=3000.0, posicao=0, vitorias=0)
    j3 = Jogador(numero=3, nome='Cauteloso', saldo=3000.0, posicao=0, vitorias=0)
    j4 = Jogador(numero=4, nome='Aleatório', saldo=3000.0, posicao=0, vitorias=0)
    jogadores = [j1, j2, j3, j4]

    total_simulacoes = 2 # 300
    total_timeout = 0
    total_turnos = 0
    j1.vitorias = 0
    j2.vitorias = 0
    j3.vitorias = 0
    j4.vitorias = 0
    for simulacao in range(total_simulacoes):
        
        j1.saldo = 3000.0
        j1.posicao = 0
        
        j2.saldo = 3000.0
        j2.posicao = 0
        
        j3.saldo = 3000.0
        j3.posicao = 0
        
        j4.saldo = 3000.0
        j4.posicao = 0

        jogadores = [j1, j2, j3, j4]
        timeout, turnos, vencedores = IniciarJogo(tabuleiro=tabuleiro, jogadores=jogadores)

        if timeout:
            total_timeout += 1
        total_turnos += turnos
        vencedor = vencedores[0]
        if vencedor.numero == 1:  # impulsivo
            j1.vitorias += 1
        elif vencedor.numero == 2:  # exigente
            j2.vitorias += 1
        elif vencedor.numero == 3:  # cauteloso
            j3.vitorias += 1
        elif vencedor.numero == 4:  # aleatório
            j4.vitorias += 1

    print('Quantidades partidas terminam por time out (1000 rodadas):', total_timeout)
    print('Média de turnos demora uma partida:', round(total_turnos / total_simulacoes))
    print('Porcentagem de vitórias do comportamento do jogador Impulsivo:', round((j1.vitorias / total_simulacoes) * 100, 2), "%")
    print('Porcentagem de vitórias do comportamento do jogador Exigente:', round((j2.vitorias / total_simulacoes) * 100, 2), "%")
    print('Porcentagem de vitórias do comportamento do jogador Cauteloso:', round((j3.vitorias / total_simulacoes) * 100, 2), "%")
    print('Porcentagem de vitórias do comportamento do jogador Aleatório:', round((j4.vitorias / total_simulacoes) * 100, 2), "%")
    vencedores = sorted(jogadores, key=lambda x: x.vitorias, reverse=True)
    print('o comportamento que mais vence:', vencedores[0].nome)


if __name__ == '__main__':
    main()


# python main.py
