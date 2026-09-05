from sqladmin import Admin, ModelView

from database.models.main_models import Worker


def admin_setup(app, engine):
    admin = Admin(app, engine)


    class WorkerAdmin(ModelView, model=Worker):
        column_list = [Worker.id,
                       Worker.name, 
                       Worker.password,
                       Worker.grades]


    admin.add_view(WorkerAdmin)