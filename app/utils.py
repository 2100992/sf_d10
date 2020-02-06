from slugify import slugify

def make_unique_slug(model, text):
    slug = slugify(text)
    counter = 0
    str_counter = ''

    while model.objects.filter(slug=slug+str_counter).count():
        print(slug+str_counter)
        counter += 1
        str_counter = str(counter)
    return slug + str_counter
