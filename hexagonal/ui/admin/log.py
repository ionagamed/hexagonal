from hexagonal import app
from hexagonal.auth.permissions import required_permission, Permission
from flask import render_template
from hexagonal import LogEntry


@app.route('/admin/logs')
@required_permission(Permission.manage)
def logs():
    entries = LogEntry.query.all()
    return render_template('admin/log.html', entries=entries)
