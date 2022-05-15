from loguru import logger
import time
import datetime as dt
import logging, threading, time, traceback, uuid
import pymqi
from dotenv import load_dotenv


def get_ini_proc() -> float:
    return time.time()

def get_fim_proc(hora: float = 0.0, texto: str = 'Tempo', logar: bool = True) -> None:
    elapsed = time.time() - hora
    msg = f'{texto}: {str(dt.timedelta(seconds=elapsed))}'
    if logar: logging.info(msg=msg)
    else: return msg

def decimal_to_str(valor: float=0.00) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def inteiro_to_str(valor: float=0.00) -> str:
    return f"{valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

def teste_put(queue_manager: str, channel: str, conn_info: str, queue_name: str, user: str, password: str, message: str):
    try:

        message = message.encode("utf-8")

        # Get Message Options
        opts = pymqi.PMO()
        opts.Options = pymqi.CMQC.MQPMO_SYNCPOINT + pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING

        # Message Descriptor
        md = pymqi.MD()
        md.Priority = 2
        md.Format = pymqi.CMQC.MQFMT_STRING
        md.MQPER_PERSISTENT = pymqi.CMQC.MQPER_PERSISTENT
        # md.CodedCharSetId = pymqi.CMQC.MQCCSI_Q_MGR
        # md.Encoding = pymqi.CMQC.MQENC_NATIVE
        # md.MsgType = pymqi.CMQC.MQMT_DATAGRAM
        # md.MsgId = pymqi.CMQC.MQMI_NONE
        # md.CorrelId = pymqi.CMQC.MQCI_NONE

        qmgr = None
        if not user and not password: qmgr = pymqi.connect(queue_manager=queue_manager, channel=channel, conn_info=conn_info)
        if user and password: qmgr = pymqi.connect(queue_manager=queue_manager, channel=channel, conn_info=conn_info, user=user, password=password)
        try:
            queue = pymqi.Queue(qmgr, queue_name)
            try:

                queue.put(message, md, opts)
                qmgr.commit()
                logging.info(f'Message Put: {message.decode(encoding="utf-8", errors="ignore")} - MsgId: {md.MsgId}')

                # max = 1_000 # 1_000 # 1_000_000
                # for num in range(max):
                #     queue.put(message, md, opts)
                #     qmgr.commit()  # qmgr.commit()  # qmgr.backout()
                #     if (num % 100) == 0:  # if (num % 100_000) == 0:
                #         logging.info(f'Message Put {inteiro_to_str(valor=num)}/{inteiro_to_str(valor=max)}')

            finally:
                queue.close()
        finally:
            qmgr.disconnect()

    except pymqi.MQMIError as e:
        if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_HOST_NOT_AVAILABLE:
            logging.error(f'Error host Put: {e}')
        elif e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
            pass # No messages, that is OK, we can ignore it.
        else:
            raise # Some other error condition.
    except Exception as e:
        logging.error(f'Error Put: {e}')


def teste_get(queue_manager: str, channel: str, conn_info: str, queue_name: str, user: str, password: str):
    try:

        message = ''

        # Get Message Options
        opts = pymqi.GMO()
        opts.Options = pymqi.CMQC.MQPMO_SYNCPOINT + pymqi.CMQC.MQGMO_FAIL_IF_QUIESCING + pymqi.CMQC.MQGMO_WAIT
        opts.WaitInterval = 5000  # 5 seconds

        # Message Descriptor
        md = pymqi.MD()

        qmgr = None
        if not user and not password: qmgr = pymqi.connect(queue_manager=queue_manager, channel=channel, conn_info=conn_info)
        if user and password: qmgr = pymqi.connect(queue_manager=queue_manager, channel=channel, conn_info=conn_info, user=user, password=password)
        try:
            queue = pymqi.Queue(qmgr, queue_name)
            try:
                max = 1_000_000
                num = 0
                while True:
                    try:
                        message = queue.get(None, md, opts)
                        qmgr.commit()  # qmgr.commit()  # qmgr.backout()
                        logging.info(f'Message Get: {message.decode(encoding="utf-8", errors="ignore")} - MsgId: {md.MsgId}')
                        # num += 1
                        # if (num % 100_000) == 0: logging.info(f'Message Get {inteiro_to_str(valor=num)}/{inteiro_to_str(valor=max)}')
                    except pymqi.MQMIError as e:
                        if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
                            break  # No messages, that is OK, we can ignore it.
                        else:
                            raise # Some other error condition.
            finally:
                queue.close()
        finally:
            qmgr.disconnect()

    except pymqi.MQMIError as e:
        if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_HOST_NOT_AVAILABLE:
            logging.error(f'Error host Get: {e}')
        elif e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_NO_MSG_AVAILABLE:
            pass # No messages, that is OK, we can ignore it.
        else:
            raise # Some other error condition.
    except Exception as e:
        logging.error(f'Error Get: {e}')






def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()


        logging.basicConfig(level=logging.INFO)

        # QM Local
        user = ''
        password = ''
        queue_manager = 'QM.04358798.01' #  QM.04358798.01 jd list = 1514 #  QM.00038166.01  bc list = 1515
        channel = 'QM.04358798.01'
        conn_info = 'localhost(1514)'
        queue_name = 'FL.INT.ENV'
        dynamic_queue_prefix = 'MY.REPLIES.*' # lease reply to a dynamic queue, thanks.
        request_queue = 'TEST.1' # lease reply to a dynamic queue, thanks.
        message = 'Hello from Python!'

        # QM Docker
        user = 'admin'
        password = 'Admin123'
        queue_manager = 'QM1'
        channel = 'DEV.ADMIN.SVRCONN'
        conn_info = '127.0.0.1(2414)'
        queue_name = 'DEV.QUEUE.1'
        message = 'Hello from Python!'

        start = get_ini_proc()
        teste_put(queue_manager=queue_manager, channel=channel, conn_info=conn_info, queue_name=queue_name, user=user, password=password, message=message)
        logging.info(msg=get_fim_proc(hora=start, texto=f'Tempo Put', logar=False))

        logging.info(f'')

        start = get_ini_proc()
        teste_get(queue_manager=queue_manager, channel=channel, conn_info=conn_info, queue_name=queue_name, user=user, password=password)
        logging.info(msg=get_fim_proc(hora=start, texto=f'Tempo Get', logar=False))

        # CARREGAR - 1Milhão
        # DELPHI = 00:11:10.586000
        # PYTHON = 00:00:00.000000

        # PUT QM - 1Milhão
        # DELPHI = 00:35:24.382000
        # PYTHON = 00:12:57.995484

        # GET QM - 1Milhão
        # DELPHI = 00:00:00.000000
        # PYTHON = 00:15:03.252933

        # GERAR - 1Milhão
        # DELPHI = 00:00:00.000000
        # PYTHON = 00:00:00.000000

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Done in {end_time:.2f}s")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')



if __name__ == '__main__':
    main()


# https://dsuch.github.io/pymqi/examples.html
# https://python.hotexamples.com/pt/examples/pymqi/-/md/python-md-function-examples.html
# https://dzone.com/articles/splendid-state-python-and



'''

constructor TJDMQMensagem.MQAX_Create(MQSessao: MQSession);
FMQAX_MQMsg := (MQSessao.AccessMessage as MQMessage);
FFormatoMsg := fm_MQFMT_NONE;
FMQAX_MQMsg.Format := FormatoMsgtoMQAXFormatStr(FFormatoMsg);
FMQAX_MQMsg.MessageType := MQMT_DATAGRAM;
FMQAX_MQMsg.Report := MQRO_NONE;
FMQAX_MQMsg.ReplyToQueueManagerName := '';
FMQAX_MQMsg.ReplyToQueueName := '';
FVersaoMQ := 6;


tpAberturaFila = (afSomentePut, afSomenteGet, afPutGet);
function TJDMQFila.AbrirFilaMQ(const NomeFila: AnsiString; OpcoesAbertura: Integer; QueueManager, QueueManagerRemoto, UserID: AnsiString): Boolean;
FMQAX_QueueFila := (FMQAX_QMgr.AccessQueue(NomeFila, OpcsAbertura, QueueManager, QueueManagerRemoto, UserID) as MQQueue);


Result := ReceberMensagemMQ(MQGMO_SYNCPOINT, RecMensagemID, RecMsgRelacionadaID);
MQGetOpcoes.Options := MQGetOpcoes.Options + MQGMO_WAIT;
MQGetOpcoes.WaitInterval := FGETIntervaloMSeg;

'''

# py -3 -m venv .venv
# python -m pip install --upgrade setuptools
# python -m pip install --upgrade wheel
# python -m pip install --upgrade pymqi
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
