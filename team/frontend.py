"""Defines the web routes of the website.

For actual content generation see the content.py module.
"""
from flask import Blueprint, render_template, jsonify, request, redirect, current_app, flash, abort, url_for
from flask_nav.elements import Navbar, Link, View
from flask_login import (current_user, login_required, login_user,
                         logout_user)
from .content import get_cluster_plot, search_gene_names, \
    get_mch_scatter, get_mch_box, get_mch_box_two_species, \
    find_orthologs, FailToGraphException, get_corr_genes, \
    gene_id_to_name, randomize_cluster_colors, get_mch_heatmap
from . import nav
from . import cache, db, mail
from .email import send_email
from os import walk
from .forms import LoginForm, ChangeUserEmailForm, ChangeAccountTypeForm, InviteUserForm, CreatePasswordForm
from .user import User, Role
from .decorators import admin_required
from flask_rq import get_queue
from flask_mail import Mail, Message

frontend = Blueprint('frontend', __name__) # Flask "bootstrap"

# Find all the samples in the data directory
dir_list = next(walk(current_app.config['DATA_DIR']))[1]

dir_list_links=[Link(x, x) for x in dir_list]


nav.register_element('frontend_top',
                     Navbar('',*dir_list_links))

# Visitor routes
@frontend.route('/')
def index():
    # Index is not needed since this site is embedded as a frame
    # We use JS redirect b/c reverse proxy will be confused about subdirectories
    html = \
    """To be redirected manually, click <a href="./hsa">here</a>.
    <script>
        window.location = "./hsa"; 
        window.location.replace("./hsa");
    </script>
    """
    return html
    
    # TODO: May need to switch to code below 
    #    depending on how to deal w/ published data

    # return \
    # """
    # To be redirected manually, click <a href="./human_combined">here</a>.' + \
    # <script>
    #      window.location = "./human_combined"; 
    #      window.location.replace("./human_combined");
    # </script>
    # """

@frontend.route('/<species>')
def species(species):
    return render_template('speciesview.html', species=species)

@frontend.route('/standalone/<species>/<gene>')
def standalone(species, gene):  # View gene body mCH plots alone
    return render_template('mch_standalone.html', species=species, gene=gene)


@frontend.route('/compare/<mmu_gid>/<hsa_gid>')
def compare(mmu_gid, hsa_gid):
    return render_template('compareview.html', mmu_gid=mmu_gid, hsa_gid=hsa_gid)


@frontend.route('/box_combined/<mmu_gid>/<hsa_gid>')
def box_combined(mmu_gid, hsa_gid):
    return render_template(
        'combined_box_standalone.html', mmu_gid=mmu_gid, hsa_gid=hsa_gid)


# API routes
@cache.cached(timeout=3600)
@frontend.route('/plot/cluster/<species>/<grouping>')
def plot_cluster(species, grouping):
    try:
        return jsonify(get_cluster_plot(species, grouping))
    except FailToGraphException:
        return 'Failed to produce cluster plot. Contact maintainer.'

@cache.cached(timeout=3600)
@frontend.route('/plot/mch/<species>/<gene>/<level>/<ptile_start>/<ptile_end>')
def plot_mch_scatter(species, gene, level, ptile_start, ptile_end):
    try:
        return get_mch_scatter(species, gene, level,
                               float(ptile_start), float(ptile_end))
    except (FailToGraphException, ValueError) as e:
        print(e)
        return 'Failed to produce mCH levels scatter plot. Contact maintainer.'


@cache.cached(timeout=3600)
@frontend.route('/plot/box/<species>/<gene>/<level>/<outliers_toggle>')
def plot_mch_box(species, gene, level, outliers_toggle):
    if outliers_toggle == 'outliers':
        outliers = True
    else:
        outliers = False

    try:
        return get_mch_box(species, gene, level, outliers)
    except (FailToGraphException, ValueError) as e:
        print(e)
        return 'Failed to produce mCH levels box plot. Contact maintainer.'


@cache.cached(timeout=3600)
@frontend.route(
    '/plot/box_combined/<species>/<gene_mmu>/<gene_hsa>/<level>/<outliers_toggle>')
def plot_mch_box_two_species(species, gene_mmu, gene_hsa, level, outliers_toggle):
    if outliers_toggle == 'outliers':
        outliers = True
    else:
        outliers = False

    try:
        return get_mch_box_two_species(species, gene_mmu, gene_hsa, level, outliers)
    except (FailToGraphException, ValueError) as e:
        print(e)
        return 'Failed to produce mCH levels box plot. Contact maintainer.'


@cache.cached(timeout=3600)
@frontend.route('/gene/names/<species>')
def search_gene_by_name(species):
    query = request.args.get('q', 'MustHaveAQueryString')
    return jsonify(search_gene_names(species, query))


@cache.cached(timeout=3600)
@frontend.route('/gene/id/<species>')
def search_gene_by_id(species):
    query = request.args.get('q', 'MustHaveAQueryString')
    return jsonify(gene_id_to_name(species, query))


@frontend.route('/gene/orthologs/<species>/<geneID>')
def orthologs(species, geneID):
    geneID = geneID.split('.')[0]
    if species == 'mmu':
        return jsonify(find_orthologs(mmu_gid=geneID))
    else:
        return jsonify(find_orthologs(hsa_gid=geneID))
    

@frontend.route('/gene/corr/<species>/<geneID>')
def correlated_genes(species, geneID):
    return jsonify(get_corr_genes(species,geneID))


@frontend.route('/plot/randomize_colors')
def randomize_colors():
    return jsonify(randomize_cluster_colors())


@frontend.route('/plot/heat/<species>/<level>/<ptile_start>/<ptile_end>')
def plot_mch_heatmap(species, level, ptile_start, ptile_end):
    query = request.args.get('q', 'MustHaveAQueryString')
    return get_mch_heatmap(species, level, ptile_start, ptile_end, query)

@frontend.route('/tabular/ensemble')
def tabular_screen():
    return render_template('tabular_ensemble.html')

@frontend.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and \
                user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You are now logged in. Welcome back!', 'form-error')
        else:
            flash('Invalid email or password.', 'form-error')
    return render_template('account/login.html', form=form)


@frontend.route('/admin')
@login_required
@admin_required
def admin():
    """Admin dashboard page."""
    return render_template('admin/index.html')

@frontend.route('/users')
@login_required
@admin_required
def registered_users():
    """View all registered users."""
    users = User.query.all()
    roles = Role.query.all()
    return render_template(
        'admin/registered_users.html', users=users, roles=roles)

@frontend.route('/new-user', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    """Create a new user."""
    return render_template('admin/new_user.html')

@frontend.route('/user/<int:user_id>')
@frontend.route('/user/<int:user_id>/info')
@login_required
@admin_required
def user_info(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@frontend.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@admin_required
def change_user_email(user_id):
    """Change a user's email."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Email for user {} successfully changed to {}.'
              .format(user.full_name(), user.email), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)

@frontend.route('/user/<int:user_id>/delete')
@login_required
@admin_required
def delete_user_request(user_id):
    """Request deletion of a user's account."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@frontend.route('/user/<int:user_id>/change-account-type', methods=['GET', 'POST'])
@login_required
@admin_required
def change_account_type(user_id):
    """Change a user's account type."""
    if current_user.id == user_id:
        flash('You cannot change the type of your own account. Please ask '
              'another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))

    user = User.query.get(user_id)
    if user is None:
        abort(404)
    form = ChangeAccountTypeForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('Role for user {} successfully changed to {}.'
              .format(user.full_name(), user.role.name), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@frontend.route('/invite-user', methods=['GET', 'POST'])
@login_required
@admin_required
def invite_user():
    """Invites a new user to create an account and set their own password."""
    form = InviteUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'frontend.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)
        # get_queue().enqueue(
        #     send_email,
        #     recipient=user.email,
        #     subject='You Are Invited To Join',
        #     template='email/invite',
        #     user=user,
        #     invite_link=invite_link, )
        send_email(recipient=user.email,subject='You Are Invited To Join',template='email/invite',user=user,invite_link=invite_link)
        flash('User {} successfully invited'.format(user.full_name()),
              'form-success')
    return render_template('admin/new_user.html', form=form)


@frontend.route(
    '/join-from-invite/<int:user_id>/<token>', methods=['GET', 'POST'])
def join_from_invite(user_id, token):
    """
    Confirm new user's account with provided token and prompt them to set
    a password.
    """
    if current_user is not None and current_user.is_authenticated:
        flash('You are already logged in.', 'error')
        return redirect(url_for('frontend.index'))

    new_user = User.query.get(user_id)
    if new_user is None:
        return redirect(404)

    if new_user.password_hash is not None:
        flash('You have already joined.', 'error')
        return redirect(url_for('main.index'))

    if new_user.confirm_account(token):
        form = CreatePasswordForm()
        if form.validate_on_submit():
            new_user.password = form.password.data
            db.session.add(new_user)
            db.session.commit()
            flash('Your password has been set. After you log in, you can '
                  'go to the "Your Account" page to review your account '
                  'information and settings.', 'success')
            return redirect(url_for('frontend.login'))
        return render_template('account/join_invite.html', form=form)
    else:
        flash('The confirmation link is invalid or has expired. Another '
              'invite email with a new link has been sent to you.', 'error')
        token = new_user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user_id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=new_user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=new_user,
            invite_link=invite_link)
    return redirect(url_for('main.index'))

@frontend.route("/mail")
def send_mail():
   msg = Message('Hello', sender = 'yourId@gmail.com', recipients = ['kuppal2790@gmail.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"


