DROP TABLE m_tag_groups CASCADE;
DROP TABLE m_tags CASCADE;



delete from django_migrations where app='objects';
delete from django_migrations where app='hosts';
delete from django_migrations where app='configuration';
delete from django_migrations where app='orders';
delete from django_migrations where app='products';
delete from django_migrations where app='members';
delete from django_migrations where app='features';


--- THE DO this commands------
---- ./manage.py migrate --fake objects 0001_initial
---- ./manage.py migrate