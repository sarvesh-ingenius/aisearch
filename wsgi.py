from app import factory

app = factory.create_app()

if __name__ == "__main__":
#    app.run(host='10.80.10.150',port=20001)
    app.run()