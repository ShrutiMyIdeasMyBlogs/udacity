#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *
from datetime import date
from datetime import datetime


# TODO: connect to a local postgresql database



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='full'):
    value = value.replace('t', 'T')
    value = value.replace('z', 'Z')

    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = value
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        # format = "ee mm, dd, y h:mma"
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en_us')


app.jinja_env.filters['datetime'] = format_datetime

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
   
   #TODO: replace with real venues data.
   #      num_shows should be aggregated based on number of upcoming shows per venue.
  
    data_ = []
    location_data = []
    venues = Venue.query.all()
    city_state=[]    
    for venue in venues:    
        location_data.append((venue.name,venue.id,venue.city,venue.state))
        city_state.append((venue.city,venue.state)) 
    location_data_unique = list(set(city_state))    
    data_dict_complete = []
    for l_data in location_data:
        dict_data = {}
        for unique_loc in location_data_unique:
            if (l_data[2]== unique_loc[0] and l_data[3]== unique_loc[1]):
                dict_data["city"] = unique_loc[0]
                dict_data["state"] = unique_loc[1]
                dict_data["venue"] = {"id": l_data[1],
                                    "name": l_data[0]}
        data_dict_complete.append(dict_data) 
    data = []
    for u_val in location_data_unique:
        temp_data = {'city':u_val[0],
                    'state':u_val[1],
                    'venues':[]}
        for d in data_dict_complete:
            if d['city'] == u_val[0] and d['state'] == u_val[1]:
                temp_data['venues'].append(d['venue'])
        data.append(temp_data) 
    return render_template('pages/venues.html', areas=sorted(data, key = lambda i: i['city']))
 

@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    
    #form.getvalue('search_term')
    #text_box_value = Venue.query.get('search_term')
    #print(text_box_value)
    try:
        search_venue = request.form['search_term']   
        search = "%{}%".format(search_venue)
        venue_search_data = Venue.query.filter(Venue.name.ilike(search)).all()
    
        trial_dict = {}
        search_data = []
        venue_name = []
        for venue_data in venue_search_data:    
            search_data.append((venue_data.name,venue_data.id,venue_data.city,venue_data.state))
            venue_name.append(venue_data.name)
        unique_venue = list(set(venue_name))
        
        data_dict_complete = []
        for l_data in search_data:   
            dict_data ={}    
            dict_data["id"] = l_data[1]
            dict_data["name"] = l_data[0]
            data_dict_complete.append(dict_data)
        
        temp_dict = {"count":0,'data':[]}
        response_data = []
        for temp_venue_data in data_dict_complete:
            temp_dict['count'] = temp_dict['count']+1
            temp_dict['data'].append({'id':temp_venue_data['id'],'name':temp_venue_data['name']})
        response_data.append(temp_dict)    
        response = response_data[0]
        return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
    except:        
        return render_template('errors/404.html')
        
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
    try:    
        data_venue = Venue.query.get(venue_id)        
        today = datetime.now()
        count_upcoming = 0
        count_past = 0        
        list_start_time = []
        list_show = []
        upcoming_shows = []
        past_shows = []
        data_venue = Venue.query.get(venue_id)        
        shows = Show.query.filter_by(venue_id=venue_id)        
        past_shows_dump = shows.filter(Show.start_time < today).all()
        print(past_shows_dump)
        upcoming_shows_dump = shows.filter(Show.start_time > today).all()      
        for past_show in past_shows_dump:
            count_past += 1
            artist = Artist.query.get(past_show.artist_id)
            temp_past_show_data = {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": format_datetime(str(past_show.start_time))
                }            
            past_shows.append(temp_past_show_data)        
        for upcoming_show in upcoming_shows_dump:
            count_upcoming += 1
            artist = Artist.query.get(upcoming_show.venue_id)
            temp_upcoming_show_data = {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": format_datetime(str(upcoming_show.start_time))
                }            
            upcoming_shows.append(temp_upcoming_show_data)
        
        data = {"id":data_venue.id,
                "name":data_venue.name,
                "address":data_venue.address,
                "city": data_venue.city,
                "genres":data_venue.genres,
                "state":data_venue.state,
                "phone":data_venue.phone,
                "website":data_venue.website,
                "facebook_link":data_venue.facebook_link,
                "seeking_talent":data_venue.seeking_talent,
                "seeking_description":data_venue.seeking_description,
                "image_link":data_venue.image_link,
                "past_shows_count":count_past,
                "upcoming_shows_count":count_upcoming,
                "past_shows":past_shows,
                "upcoming_shows":upcoming_shows}
        return render_template('pages/show_venue.html', venue=data)
    except:        
        return render_template('errors/404.html')
    
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create')
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    try:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        new_venue_data = Venue(            
                name=request.form['name'],
                city=request.form['city'],
                state=request.form['state'],
                address=request.form['address'],
                website=request.form['website'],
                phone=request.form['phone'],
                image_link=request.form['image_link'],
                genres=request.form.getlist('genres'),
                facebook_link=request.form['facebook_link'],
                seeking_talent=True if "seeking_talent" in request.form.keys() else False,
                seeking_description=request.form['seeking_description'])
        db.session.add(new_venue_data)
        db.session.commit()
        return render_template('pages/home.html')
    except:
        db.session.rollback()
        return render_template('errors/404.html')
        

@app.route('/venues/delete')
def delete_venue_form():    
    form=DeleteVenueForm()
    #venue_id=request.form['id']
    #data_venue_delete = Venue.query.get(venue_id)
    return render_template('forms/delete_venue.html',form=form)


@app.route('/venues/delete', methods=['POST'])
def delete_venue():
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    
    
    venue_id = request.form['id']
    delete_venue_data = Venue.query.get(venue_id)
    if delete_venue_data:    
        venue_name = delete_venue_data.name
        db.session.delete(delete_venue_data)
        db.session.commit()
        flash('Venue ' + venue_name + ' was successfully deleted!')
    else:
        return render_template('errors/venue_id_not_found.html',venue_id=venue_id)
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    try:
        artist_data = Artist.query.all()  
        #orders = Order.query.filter_by(account_id=account.id).distinct()
        data =[]
        for artist in artist_data:
            artist_dict ={"id":artist.id,
                        "name":artist.name}
            data.append(artist_dict)
        return render_template('pages/artists.html', artists=data)
    except:
        return render_template('errors/404.html')

@app.route('/artists/search', methods=['POST'])
def search_artists():
    #TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    #seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    #search for "band" should return "The Wild Sax Band".
    try:
        search_artist = request.form['search_term']   
        search = "%{}%".format(search_artist)
        artist_search_data = Artist.query.filter(Artist.name.ilike(search)).all()    
        trial_dict = {}
        search_data = []
        artist_name = []
        for artist_data in artist_search_data:    
            search_data.append((artist_data.name,artist_data.id,artist_data.city,artist_data.state))
            artist_name.append(artist_data.name)
        unique_artist = list(set(artist_name))
        
        data_dict_complete = []
        for l_data in search_data:   
            dict_data ={}    
            dict_data["id"] = l_data[1]
            dict_data["name"] = l_data[0]
            data_dict_complete.append(dict_data)
        
        temp_dict = {"count":0,'data':[]}
        response_data = []
        for temp_artist_data in data_dict_complete:
            temp_dict['count'] = temp_dict['count']+1
            temp_dict['data'].append({'id':temp_artist_data['id'],'name':temp_artist_data['name']})
        response_data.append(temp_dict)    
        response = response_data[0] 
        return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
    except:
        return render_template('errors/404.html')
        
        
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    try:
        today = datetime.now()
        count_upcoming = 0
        count_past = 0        
        list_start_time = []
        list_show = []
        upcoming_shows = []
        past_shows = []
        data_artist = Artist.query.get(artist_id)        
        shows = Show.query.filter_by(artist_id=artist_id)
        past_shows_dump = shows.filter(Show.start_time < today).all()
        upcoming_shows_dump = shows.filter(Show.start_time > today).all()      
        for past_show in past_shows_dump:
            count_past += 1
            venue = Venue.query.get(past_show.venue_id)
            temp_past_show_data = {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": format_datetime(str(past_show.start_time))
                }            
            past_shows.append(temp_past_show_data)        
        for upcoming_show in upcoming_shows_dump:
            count_upcoming += 1
            venue = Venue.query.get(upcoming_show.venue_id)
            temp_upcoming_show_data = {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": format_datetime(str(upcoming_show.start_time))
                }            
            upcoming_shows.append(temp_upcoming_show_data)
        data = {"id":data_artist.id,
                "name":data_artist.name,          
                "city": data_artist.city,
                "genres":data_artist.genres,
                "state":data_artist.state,
                "phone":data_artist.phone,
                "website":data_artist.website,
                "facebook_link":data_artist.facebook_link,
                "seeking_venue":data_artist.seeking_venue,
                "seeking_description":data_artist.seeking_description,
                "image_link":data_artist.image_link,
                "past_shows_count":count_past,
                "upcoming_shows_count":count_upcoming,
                "past_shows":past_shows,
                "upcoming_shows":upcoming_shows
                }  
        return render_template('pages/show_artist.html', artist=data)
    except:
        return render_template('errors/404.html')
    
    
    
@app.route('/artists/delete',methods=['GET'])
def delete_artist_form():
    
    form=DeleteArtistForm() 
    return render_template('forms/delete_artist.html',form=form)


@app.route('/artists/delete', methods=['POST','DELETE'])
def delete_artist():
    # TODO: Complete this endpoint for taking a artist_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    
    # BONUS CHALLENGE: Implement a button to delete a artist on a artist Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage 
    
    artist_id = request.form['id']
    delete_artist_data = Artist.query.get(artist_id)
    if delete_artist_data:    
        artist_name = delete_artist_data.name
        db.session.delete(delete_artist_data)
        db.session.commit()
        flash('artist ' + artist_name + ' was successfully deleted!')
    else:
        return render_template('errors/artist_id_not_found.html',artist_id=artist_id)
    return render_template('pages/home.html')
    
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/edit')
def edit_artist():
    form = EditArtistForm()  
    return render_template('forms/edit_artist.html', form=form)
  
@app.route('/artists/edit',methods = ['POST'])
def edit_artist_id():
    id = request.form['id']  
    return redirect(url_for('edit_artist_submission', artist_id=id))

@app.route('/artists/<int:artist_id>/edit')
def edit_artist_data(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes   
    form = EditArtistDetailsForm()  
    artist_edit_data = Artist.query.get(artist_id)
    if artist_edit_data:
        return render_template('forms/edit_artist_second_page.html', form=form, artist=artist_edit_data)
    else:        
        return render_template('errors/artist_id_not_found.html', artist_id=artist_id)


@app.route('/artists/<int:artist_id>/edit',methods = ['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes    
    db.session.query(Artist).filter(Artist.id == artist_id).update(
    {'name': request.form['name'],
    'city': request.form['city'],
    'state': request.form['state'],            
    'website': request.form['website'],
    'phone': request.form['phone'],
    'image_link': request.form['image_link'],
    'genres': request.form.getlist('genres'),
    'facebook_link': request.form['facebook_link'],
    'seeking_venue': True if "seeking_venue" in request.form.keys() else False,
    'seeking_description':request.form['seeking_description']})
    db.session.commit()
    return render_template('pages/home.html')
    
@app.route('/venues/edit')    
def edit_venue():
    form = EditVenueForm()
    return render_template('forms/edit_venue.html', form = form)
    
@app.route('/venues/edit',methods = ['POST'])    
def edit_venue_id():
    venue_id = request.form['id']    
    return redirect(url_for('edit_venue_submission', venue_id = venue_id))
    
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue_submission(venue_id):
    form = EditVenueDetailsForm()
    edit_venue_data = Venue.query.get(venue_id)
    if edit_venue_data:    
        return render_template('forms/edit_venue_second_page.html',form=form,venue = edit_venue_data)
    else:
        return render_template('errors/venue_id_not_found.html', venue_id=venue_id)        
        
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_data(venue_id):
    #TODO: take values from the form submitted, and update existing
    #venue record with ID <venue_id> using the new attributes
    try:
        db.session.query(Venue).filter(Venue.id == venue_id).update({
        'name': request.form['name'],
        'city': request.form['city'],
        'state': request.form['state'], 
        'address': request.form['address'],
        'website': request.form['website'],
        'phone': request.form['phone'],
        'image_link': request.form['image_link'],
        'genres': request.form.getlist('genres'),
        'facebook_link': request.form['facebook_link'],
        'seeking_talent': True if "seeking_talent" in request.form.keys() else False,
        'seeking_description':request.form['seeking_description']})
        db.session.commit()
        return render_template('pages/home.html')
    except:
        db.session.rollback()
        return render_template('errors/404.html')
        
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    try:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        # TODO: modify data to be the data object returned from db insertion
        new_artist_data = Artist(            
                    name=request.form['name'],
                    city=request.form['city'],
                    state=request.form['state'],            
                    website=request.form['website'],
                    phone=request.form['phone'],
                    image_link=request.form['image_link'],
                    genres=request.form.getlist('genres'),
                    facebook_link=request.form['facebook_link'],
                    seeking_venue=True if "seeking_venue" in request.form.keys() else False,
                    seeking_description=request.form['seeking_description'])
        db.session.add(new_artist_data)
        db.session.commit()
        return render_template('pages/home.html')
    # on successful db insert, flash success
    except:
        db.session.rollback()
        return render_template('errors/404.html')
        
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
# displays list of shows at /shows
# TODO: replace with real venues data.
#       num_shows should be aggregated based on number of upcoming shows per venue.
    try:  
        data = []
        for a, s, v in db.session.query(Artist, Show, Venue).filter(Artist.id == Show.artist_id).filter(Venue.id == Show.venue_id).all():
            temp_data = {}
            temp_data["venue_id"] = v.id
            temp_data["venue_name"] = v.name
            temp_data["artist_id"] = a.id
            temp_data["artist_name"] = a.name
            temp_data["artist_image_link"] = a.image_link
            temp_data["start_time"] = format_datetime(str(s.start_time))
            data.append(temp_data)   
        return render_template('pages/shows.html', shows=data)
    except:        
        return render_template('errors/404.html')
        
        
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    
    # on successful db insert, flash success
    
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    artist_id = request.form['artist_id']   
    venue_id = request.form['venue_id']   
    start_time = request.form['start_time']  
    try :
        new_show_data = Show(artist_id=request.form['artist_id'], venue_id=request.form['venue_id'],
            start_time=request.form['start_time'])                
        db.session.add(new_show_data)
        db.session.commit()
        flash('Show was successfully listed!')
        return render_template('pages/home.html') 
        
    except sqlalchemy.exc.IntegrityError as e:
       data = [artist_id,venue_id]       
       return render_template('errors/artist_venue_id_not_found.html',artist_id = data[0], venue_id = data[1])
    except:       
       return not_found_error(404)
   
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
