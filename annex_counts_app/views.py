# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
# from annex_counts_app.lib.shib_auth import shib_login  # decorator
from . import settings_app
from annex_counts_app.lib import updater as updt_hlpr
from annex_counts_app.lib import view_info_helper
from annex_counts_app.lib.stats import StatsBuilder
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


log = logging.getLogger(__name__)


def stats( request ):
    """ Prepares stats for given dates; returns json. """
    # return HttpResponse( 'stats coming' )

    log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()

    stats_builder = StatsBuilder()

    # dummy_output = stats_builder.generate_dummy_output()
    # return HttpResponse( dummy_output, content_type='application/javascript; charset=utf-8' )

    ## grab & validate params
    if stats_builder.check_params( request.GET, request.scheme, request.META['HTTP_HOST'], rq_now ) == False:
        return HttpResponseBadRequest( stats_builder.output_jsn, content_type=u'application/javascript; charset=utf-8' )
    ## query records for period (parse them via source)
    # requests = stats_builder.run_query()
    ## process results
    # data = stats_builder.process_results( requests )

    jsn_data = stats_builder.generate_dummy_output( request.GET, request.scheme, request.META['HTTP_HOST'], rq_now )
    return HttpResponse( jsn_data, content_type=u'application/javascript; charset=utf-8' )

    ## build response
    # stats_builder.build_response( data, request.scheme, request.META['HTTP_HOST'], request.GET )
    # return HttpResponse( stats_builder.output, content_type=u'application/javascript; charset=utf-8' )


def updater( request ):
    """ Updates stats db. """
    log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    if updt_hlpr.check_validity( request ) is False:
        return HttpResponseBadRequest( '400 / Bad Request' )
    foo = updt_hlpr.prep_counts( request )
    # ( dt: datetime.date, hay_accessions: int, hay_refiles: int, non_hay_accessions: int, non_hay_refiles: int ) = updt_hlpr.prep_counts( request )
    ( dt, hay_accessions, hay_refiles, non_hay_accessions, non_hay_refiles ) = updt_hlpr.prep_counts( request )


# -------
# helpers
# -------

def info( request ):
    """ Returns basic data including branch & commit. """
    # log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()
    commit = view_info_helper.get_commit()
    branch = view_info_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    resp_now = datetime.datetime.now()
    taken = resp_now - rq_now
    context_dct = view_info_helper.make_context( request, rq_now, info_txt, taken )
    output = json.dumps( context_dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def error_check( request ):
    """ For an easy way to check that admins receive error-emails (in development).
        To view error-emails in runserver-development:
        - run, in another terminal window: `python -m smtpd -n -c DebuggingServer localhost:1026`,
        - (or substitue your own settings for localhost:1026)
    """
    if project_settings.DEBUG == True:
        1/0
    else:
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )


# @shib_login
# def login( request ):
#     """ Handles authNZ, & redirects to admin.
#         Called by click on login or admin link. """
#     next_url = request.GET.get( 'next', None )
#     if not next_url:
#         redirect_url = reverse( settings_app.POST_LOGIN_ADMIN_REVERSE_URL )
#     else:
#         redirect_url = request.GET['next']  # will often be same page
#     log.debug( 'redirect_url, ```%s```' % redirect_url )
#     return HttpResponseRedirect( redirect_url )
