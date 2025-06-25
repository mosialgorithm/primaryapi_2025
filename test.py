# image = files['image']
    # # if image and allowed_image(image.filename):
    #     article = Article()
    #     # 
    #     # directory = Path(os.path.join(app.config['UPLOAD_IMAGE'], f'{article.id}'))
    #     # directory.mkdir(parents=True, exist_ok=True)
    #     # location = os.path.join(directory ,secure_filename(image.filename))
    #     # 
    #     # article.image = location
    #     article.title = user_data['title']
    #     article.body = user_data['body']
    #     article.user_id = user_data['user_id']
    #     try:
    #         # image.save(location)
    #         article.save()
    #         return article
    #     except Exception as ex:
    #         abort(400, message=f"Error {ex} is happened !!")
    # # else:
    # #     abort(400, message='file is not standard')