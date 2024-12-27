from flask import Blueprint, render_template, request, redirect, url_for

lab9 = Blueprint('lab9', __name__)


@lab9.route('/lab9/', methods=['GET', 'POST'])
def lab():
    if request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('lab9.age', name=name))
    return render_template('lab9/lab9.html')


@lab9.route('/lab9/age/', methods=['GET', 'POST'])
def age():
    name = request.args.get('name')
    if request.method == 'POST':
        age = request.form.get('age')
        return redirect(url_for('lab9.gender', name=name, age=age))
    return render_template('lab9/age.html', name=name)


@lab9.route('/lab9/gender/', methods=['GET', 'POST'])
def gender():
    name = request.args.get('name')
    age = request.args.get('age')
    if request.method == 'POST':
        gender = request.form.get('gender')
        return redirect(url_for('lab9.preference', name=name, age=age, gender=gender))
    return render_template('lab9/gender.html', name=name, age=age)


@lab9.route('/lab9/preference/', methods=['GET', 'POST'])
def preference():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    if request.method == 'POST':
        preference = request.form.get('preference')
        return redirect(url_for('lab9.treat', name=name, age=age, gender=gender, preference=preference))
    return render_template('lab9/preference.html', name=name, age=age, gender=gender)


@lab9.route('/lab9/treat/', methods=['GET', 'POST'])
def treat():
    name = request.args.get('name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    if request.method == 'POST':
        treat = request.form.get('treat')
        return redirect(url_for('lab9.congratulations', name=name, age=age, gender=gender, preference=preference, treat=treat))
    return render_template('lab9/treat.html', name=name, age=age, gender=gender, preference=preference)


@lab9.route('/lab9/congratulations/', methods=['GET'])
def congratulations():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    gender = request.args.get('gender')
    preference = request.args.get('preference')
    treat = request.args.get('treat')

    if gender == 'male':
        pronoun = 'быстро вырос, был умным'
        gift = 'мешочек конфет' if preference == 'vkusno' and treat == 'sweat' else 'подарок сытной еды'
    else:
        pronoun = 'быстро выросла, была умной'
        gift = 'мешочек конфет' if preference == 'vkusno' and treat == 'sweat' else 'подарок сытной еды'

    image = 'candies.png' if treat == 'sweat' else 'cake.png'

    return render_template('lab9/congratulations.html', name=name, pronoun=pronoun, gift=gift, image=image)
