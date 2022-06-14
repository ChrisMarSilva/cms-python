from math import trunc
from loguru import logger
import time
import datetime as dt


def teste_01_quick_dash():
    try:

        from dashing import QuickDash

        d = QuickDash()
        d.status = "Running..."
        d.logs.append("Started")

        for progress in range(100):
            d.gauges['progess'] = progress
            if progress % 10 == 0:
                d.logs.append("Started")
            time.sleep(0.05)

        d.status = "Done!"
        time.sleep(1)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_02_quick_dash():
    try:

        # from dashing import *
        from dashing import HSplit, VSplit, HGauge, VGauge, ColorRangeVGauge, Text, Log, VChart, HChart, HBrailleChart, HBrailleFilledChart
        from time import sleep, time
        import math

        ui = HSplit(
                VSplit(
                    HGauge(val=50, title="only title", border_color=5),
                    HGauge(label="only label", val=20, border_color=5),
                    HGauge(label="only label", val=30, border_color=5),
                    HGauge(label="only label", val=50, border_color=5),
                    HGauge(label="only label", val=80, border_color=5),
                    HGauge(val=20),
                    HGauge(label="label, no border", val=55),
                    HSplit(
                        VGauge(val=0, border_color=2),
                        VGauge(val=5, border_color=2),
                        VGauge(val=30, border_color=2),
                        VGauge(val=50, border_color=2),
                        VGauge(val=80, border_color=2, color=4),
                        VGauge(val=95, border_color=2, color=3),
                        ColorRangeVGauge(val=100, border_color=2, colormap=((33, 2), (66, 3), (100, 1))),
                    )
                ),
                VSplit(
                    Text('Hello World,\nthis is dashing.', border_color=2),
                    Log(title='logs', border_color=5),
                    VChart(border_color=2, color=2),
                    HChart(border_color=2, color=2),
                    HBrailleChart(border_color=2, color=2),
                    # HBrailleFilledChart(border_color=2, color=2),
                ),
                title='Dashing',
            )
        log = ui.items[1].items[1]
        vchart = ui.items[1].items[2]
        hchart = ui.items[1].items[3]
        bchart = ui.items[1].items[4]
        # bfchart = ui.items[1].items[5]
        log.append("0 -----")
        log.append("1 Hello")
        log.append("2 -----")
        prev_time = time()
        for cycle in range(0, 200):
            ui.items[0].items[0].value = int(50 + 49.9 * math.sin(cycle / 80.0))
            ui.items[0].items[1].value = int(50 + 45 * math.sin(cycle / 20.0))
            ui.items[0].items[2].value = int(50 + 45 * math.sin(cycle / 30.0 + 3))

            vgauges = ui.items[0].items[-1].items
            for gaugenum, vg in enumerate(vgauges):
                vg.value = 50 + 49.9 * math.sin(cycle / 12.0 + gaugenum)

            t = int(time())
            if t != prev_time:
                log.append("%s" % t)
                prev_time = t
            vchart.append(50 + 50 * math.sin(cycle / 16.0))
            hchart.append(99.9 * abs(math.sin(cycle / 26.0)))
            bchart.append(50 + 50 * math.sin(cycle / 6.0))
            # bfchart.append(50 + 50 * math.sin(cycle / 16.0))
            ui.display()

            sleep(1.0/25)# sleep(0.5)  # sleep(1.0/25)# 

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def bytes_to_gigas(value):
    # return f'{value / 1024 / 1024 / 1024: .2f}GB'
    return value / 1024 / 1024 / 1024

def teste_03_quick_dash():
    try:

        from psutil import virtual_memory, swap_memory, cpu_percent, sensors_battery, disk_io_counters, disk_partitions, disk_usage, net_io_counters, net_if_addrs, users, boot_time, pids, process_iter
        from dashing import HSplit, VSplit, HGauge, VGauge, Text
        from datetime import datetime
        from time import sleep

        ui = HSplit(  # ui
            VSplit(  # ui.items[0]
                Text(  # ui.items[0].items[0]
                    ' ',
                    border_color=9,
                    title='Processos',
                    color=7,
                ),
                HSplit(   # ui.items[0].items[1]
                    VGauge(title='RAM'),  # ui.items[0].items[1].items[0]
                    VGauge(title='SWAP'),  # ui.items[0].items[1].items[1]
                    title='Memória',
                    border_color=3
                ),
            ),
            VSplit(  # ui.items[1]
                    HGauge(title="CPU %"),  # ui.items[1].items[0]
                    HGauge(title="cpu_1"),  # ui.items[1].items[1]
                    HGauge(title="cpu_2"),  # ui.items[1].items[2]
                    HGauge(title="cpu_3"),  # ui.items[1].items[3]
                    HGauge(title="cpu_4"),  # ui.items[1].items[4]
                    # HGauge(title="Temp."),  # ui.items[1].items[5]
                    title="CPU", 
                    border_color=11,
                ),
                VSplit(  # ui.items[2]
                    Text(' ', title='Outros', border_color=4, color=7),  # ui.items[2].items[0]
                    Text(' ', title='Disco', border_color=6, color=7), # ui.items[2].items[1]
                    Text(' ', title='Rede', border_color=4, color=7), # ui.items[2].items[2]
                ),
            )

        while True:

            # # Processos
            proc_tui = ui.items[0].items[0]
            p_list = []
            for proc in process_iter():
                proc_info = proc.as_dict(['name', 'cpu_percent', 'memory_percent'])
                if proc_info['name'] == 'System Idle Process':
                    continue
                if proc_info['cpu_percent'] > 0:
                    p_list.append(proc_info)

            proc_tui.text = f"{'Nome':<20}{'CPU':<10}Memória"

            ordenados = sorted(p_list, key=lambda p: p['cpu_percent'], reverse=True)[:10]
            for proc in ordenados:
                proc_tui.text += f"\n{proc['name']:<20} {proc['cpu_percent']/4:<10} {proc['memory_percent']:.2f}"

            # # Memoria
            mem_tui = ui.items[0].items[1]

            # Ram
            ram_tui = mem_tui.items[0]
            ram_tui.value = virtual_memory().percent
            ram_tui.title = f'RAM {ram_tui.value} %'

            # Swap
            swap_tui = mem_tui.items[1]
            swap_tui.value = swap_memory().percent
            swap_tui.title = f'SWAP {swap_tui.value} %'

            # # CPU
            cpu_tui = ui.items[1]

            # CPU %
            cpu_percent_tui = cpu_tui.items[0]
            ps_cpu_percent = cpu_percent()
            cpu_percent_tui.value = ps_cpu_percent
            cpu_percent_tui.title = f'CPU {cpu_percent_tui.value} %'

            # Porcentagem dos cores
            cores_tui = cpu_tui.items[1:5]
            ps_cpu_percent = cpu_percent(percpu=True)
            for i, (core, value) in enumerate(zip(cores_tui,ps_cpu_percent)):
                core.value = value
                core.title = f'cpu_{i+1} {core.value} %'

            # NAO TEM PARA WIN
            # CPU Temp
            # cpu_temp_tui = cpu_tui.items[6]
            # ps_cpu_temp = psutil.sensors_temperatures()['coretemp'][0]
            # cpu_temp_tui.value = ps_cpu_temp.current
            # cpu_temp_tui.title = f'CPU Temp. {cpu_temp_tui.value}C'

            # # Outros
            outros_tui = ui.items[2].items[0]
            outros_tui.text = f'Bateria: {sensors_battery().percent}%'
            outros_tui.text += f'\nUsuário: {users()[0].name}'
            boot = datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            outros_tui.text += f'\nHorário do boot: {boot}'
            outros_tui.text += f'\nProcessos: {len(pids())}'

            # # Disco
            disk_tui = ui.items[2].items[1]
            partitions = disk_partitions()
            counters = disk_io_counters(perdisk=True)
            disk_tui.text = f"{'Partição':<10}{'Uso':<5}{'Livre':<6}{'Lido':<6}{'Escrito'}"

            for partition in partitions:
                # partition_name_counter = partition.device.split('/')[-1]
                partition_name_counter = partition.device.split('/')[-1].replace(':', '').replace('\\', '')
                percent_disk_usage = disk_usage(partition.mountpoint).percent
                percent_disk_free = f'{100 - percent_disk_usage: .2f}'
                try:
                    disk_bytes = counters[partition_name_counter]
                    disk_tui.text += '\n{:<10}{:<4}{:<7}{:<6.2f}{:.2f}'.format(partition.mountpoint, percent_disk_usage, percent_disk_free, bytes_to_gigas(disk_bytes.read_bytes), bytes_to_gigas(disk_bytes.write_bytes))
                except:
                    disk_bytes = counters
                    disk_tui.text += '\n{:<10}{:<4}{:<7}{:<6.2f}{:.2f}'.format(partition.mountpoint, percent_disk_usage, percent_disk_free, bytes_to_gigas(disk_bytes['PhysicalDrive0'].read_bytes), bytes_to_gigas(disk_bytes['PhysicalDrive0'].write_bytes))

            # # Rede
            network_tui = ui.items[2].items[2]
            addrs_v4 = net_if_addrs()['Wi-Fi 2'][1]  # 'wlp2s0'[0]  # 'Wi-Fi 2'
            addrs_v6 = net_if_addrs()['Wi-Fi 2'][2]  # 'wlp2s0'[1]  # 'Wi-Fi 2'
            network_tui.text = f'IPV4: {addrs_v4.address[:30]}\n'
            network_tui.text += f'MaskV4: {addrs_v4.netmask}\n'
            network_tui.text += f'IPV6: {addrs_v6.address[:30]}\n'
            network_tui.text += f'MaskV6: {addrs_v6.netmask}\n'
            network_tui.text += f'Enviado : {bytes_to_gigas(net_io_counters().bytes_sent):.2f}GB\n'
            network_tui.text += f'Recebido: {bytes_to_gigas(net_io_counters().bytes_recv):.2f}GB\n'

            try:
                ui.display()
                sleep(1) # sleep(0.5)  #  sleep(1.0/25)  # 
            except KeyboardInterrupt:
                break

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    start_time = time.perf_counter()
    logger.info(f'Inicio') 
    try:

        # result = 'ok'
        # logger.info(f'{result=}')

        # teste_01_quick_dash()  # Erro
        # teste_02_quick_dash()
        teste_03_quick_dash()

        # import psutil
        # print(psutil.sensors_battery().percent)
        # print(psutil.disk_partitions())
        # print(psutil.disk_io_counters(perdisk=True))
        # print(psutil.net_if_addrs())

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == '__main__':
    main()

# python -m pip install --upgrade pip
# python -m pip install --upgrade psutil
# python -m pip install --upgrade py-dashing

# python main.py


'''



{
    'Conexão Local': [snicaddr(family=<AddressFamily.AF_LINK: -1>, address='00-FF-87-3E-21-61',netmask=None, broadcast=None, ptp=None), 
                        snicaddr(family=<AddressFamily.AF_INET: 2>, address='10.10.200.74', netmask='255.255.255.252', broadcast=None, ptp=None), 
                        snicaddr(family=<AddressFamily.AF_INET6: 23>, address='fe80::8979:4a1e:6e7b:ff2e', netmask=None, broadcast=None, ptp=None)
                    ], 
'Ethernet': [snicaddr(family=<AddressFamily.AF_LINK: -1>, address='64-1C-67-B2-52-B4', netmask=None, broadcast=None, ptp=None), 
            snicaddr(family=<AddressFamily.AF_INET: 2>, address='169.254.34.98', netmask='255.255.0.0', broadcast=None, ptp=None), 
            snicaddr(family=<AddressFamily.AF_INET6: 23>, address='fe80::5d26:b640:56e0:2262', netmask=None, broadcast=None, ptp=None)
            ], 
            
'vEthernet (WSL)': [snicaddr(family=<AddressFamily.AF_LINK: -1>, address='00-15-5D-E2-5B-AB', netmask=None, broadcast=None, ptp=None), 
                    snicaddr(family=<AddressFamily.AF_INET: 2>, address='172.28.0.1', netmask='255.255.240.0', broadcast=None, ptp=None), 
                    snicaddr(family=<AddressFamily.AF_INET6: 23>, address='fe80::9dc9:e1e7:dd41:c88e', netmask=None, broadcast=None, ptp=None)], 
                    
'Conexão Local* 3': [snicaddr(family=<AddressFamily.AF_LINK: -1>, address='B2-A7-B9-B3-29-4A', netmask=None, broadcast=None, ptp=None), 
                    snicaddr(family=<AddressFamily.AF_INET: 2>, address='169.254.205.111', netmask='255.255.0.0', broadcast=None, ptp=None), 
                    snicaddr(family=<AddressFamily.AF_INET6: 23>, address='fe80::a4c9:7e9e:b335:cd6f', netmask=None, broadcast=None, ptp=None)], 

'Conexão Local* 4': [snicaddr(family=<AddressFamily.AF_LINK: -1>, address='B0-A7-B9-B3-29-4A', netmask=None, broadcast=None, ptp=None), 
                    snicaddr(family=<AddressFamily.AF_INET: 2>, address='169.254.197.105', netmask='255.255.0.0', broadcast=None, ptp=None), 
                    snicaddr(family=<AddressFamily.AF_INET6: 23>, address='fe80::b901:b1a6:d2a0:c569', netmask=None, broadcast=None, ptp=None)], 
                    
'Wi-Fi 2': [snicaddr(family=<AddressFamily.AF_LINK: -1>, address='B0-A7-B9-B3-29-4A', netmask=None, broadcast=None, ptp=None), 
            snicaddr(family=<AddressFamily.AF_INET: 2>, address='192.168.1.102', netmask='255.255.255.0', broadcast=None, ptp=None), 
            snicaddr(family=<AddressFamily.AF_INET6: 23>, address='fe80::706a:ee00:f6ef:11d4', netmask=None, broadcast=None, ptp=None)], 
            
'Conexão de Rede Bluetooth': [snicaddr(family=<AddressFamily.AF_LINK: -1>, address='64-32-A8-82-26-C4', netmask=None, broadcast=None, ptp=None), 
                            snicaddr(family=<AddressFamily.AF_INET: 2>, address='169.254.31.252', netmask='255.255.0.0', broadcast=None, ptp=None), 
                            snicaddr(family=<AddressFamily.AF_INET6: 23>, address='fe80::9501:2878:7d70:1ffc', netmask=None, broadcast=None, ptp=None)], 
                            
'Loopback Pseudo-Interface 1': [snicaddr(family=<AddressFamily.AF_INET: 2>, address='127.0.0.1', netmask='255.0.0.0', broadcast=None, ptp=None), 
                                snicaddr(family=<AddressFamily.AF_INET6: 23>, address='::1', netmask=None, broadcast=None, ptp=None)
                                ]}




'''
