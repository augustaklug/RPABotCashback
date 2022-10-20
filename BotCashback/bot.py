"""
WARNING:

Please make sure you install the bot with `pip install -e .` in order to get all the dependencies
on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the bot.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install -e .`
- Use the same interpreter as the one used to install the bot (`pip install -e .`)

Please refer to the documentation for more information at https://documentation.botcity.dev/
"""

import datetime
from botcity.core import DesktopBot
# Uncomment the line below for integrations with BotMaestro
# Using the Maestro SDK
from botcity.maestro import *


class Bot(DesktopBot):
    def action(self, execution=None):
        # Uncomment to silence Maestro errors when disconnected
        if self.maestro:
            self.maestro.RAISE_NOT_CONNECTED = False

        # Fetch the Activity ID from the task:
        # task = self.maestro.get_task(execution.task_id)
        # activity_id = task.activity_id

        stores = ['Amazon', 'Americanas', 'Submarino', 'AliExpress']
        WAITING_TIME = 20000

        # Meliuz
        self.browse("https://www.meliuz.com.br/desconto")

        for store in stores:
            if not self.find( "search_meliuz", matching=0.97, waiting_time=10000):
                self.not_found("search_meliuz")
            self.click_relative(76, 17)
            self.paste(store)
            
            if not self.find( "select_meliuz", matching=0.97, waiting_time=WAITING_TIME):
                self.not_found("select_meliuz")
            self.click_relative(10, 43)

            if not self.find( "cb_meliuz", matching=0.97, waiting_time=WAITING_TIME):
                self.not_found("cb_meliuz")
            self.double_click_relative(21, 8)
            
            self.control_c()
            cb_meliuz = self.get_clipboard()
            print(f"Meliuz: {store} => {cb_meliuz}")

            if(int(cb_meliuz) > 5):
                self.send_cb_alert(execution.task_id, "Méliuz", store, cb_meliuz)

            self.maestro.new_log_entry(
                activity_label="CashbackData",
                values={
                    "datetime": datetime.datetime.now().strftime("%Y-%m-%d_%H-%M"),
                    "provider": "Méliuz",
                    "store": store,
                    "cashback": cb_meliuz
                }
            )
            self.sleep(1000)
            self.click_relative(-300,-50)
            if not self.find( "back_meliuz", matching=0.97, waiting_time=WAITING_TIME):
                self.not_found("back_meliuz")
            self.click()



        if not self.find( "addressbar", matching=0.97, waiting_time=10000):
            self.not_found("addressbar")
        self.click()
        self.paste("https://intershop.bancointer.com.br/lojas")
        self.enter(wait=1000)


        # Banco Inter
        for store in stores:
            if not self.find( "find_inter", matching=0.97, waiting_time=WAITING_TIME):
                self.not_found("find_inter")
            self.click()
            self.paste(store)
            
            if not self.find( "select_store_inter", matching=0.97, waiting_time=WAITING_TIME):
                self.not_found("select_store_inter")
            self.click_relative(106, 116)
            
            if not self.find( "cb_inter", matching=0.97, waiting_time=WAITING_TIME):
                self.not_found("cb_inter")
            self.double_click_relative(221, 31)
            self.control_c()
            cb_inter = self.get_clipboard()
            print(f"Banco Inter: {store} => {cb_inter}")

            if(int(cb_inter) > 5):
                self.send_cb_alert(execution.task_id, "Banco Inter", store, cb_inter)

            self.maestro.new_log_entry(
                activity_label="CashbackData",
                values={
                    "datetime": datetime.datetime.now().strftime("%Y-%m-%d_%H-%M"),
                    "provider": "Banco Inter",
                    "store": store,
                    "cashback": cb_inter
                }
            )
            
            if not self.find( "back_to_search_inter", matching=0.97, waiting_time=WAITING_TIME):
                self.not_found("back_to_search_inter")
            self.click()

        # Uncomment to mark this task as finished on BotMaestro
        self.maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.SUCCESS,
            message="Task Finished OK."
        )

    def not_found(self, label):
        print(f"Element not found: {label}")

    def send_cb_alert(self, task_id, provider, store, cashback):
        self.maestro.alert(task_id=task_id,
                           title=f"Cashback bom encontrado para {store}",
                           message=f"Foi encontrado um cashback de {cashback}% para {store} em {provider}",
                           alert_type=AlertType.INFO
                           )
        print("Alert Sent!")


if __name__ == '__main__':
    Bot.main()







