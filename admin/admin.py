from sqladmin import Admin, ModelView

from database.models.main_models import Worker, Boiler, Order


def admin_setup(app, engine):
    admin = Admin(app, engine)


    class WorkerAdmin(ModelView, model=Worker):
        column_list = [Worker.id,
                       Worker.name, 
                       Worker.password,
                       Worker.grades]


    class BoilerAdmin(ModelView, model=Boiler):
        column_list = [Boiler.id,
                       Boiler.name,
                       Boiler.order_id,
                       Boiler.power,
                       Boiler.work_state]


    class OrderAdmin(ModelView, model=Order):
        column_list = [Order.id,
                       Order.boiler,
                       Order.status,
                       Order.text_order,]


    admin.add_view(WorkerAdmin)
    admin.add_view(BoilerAdmin)
    admin.add_view(OrderAdmin)