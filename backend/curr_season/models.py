from django.db import models

# Create your models here.
class Stat(models.Model):
  season = models.CharField(max_length=255, default='')
  team = models.CharField(max_length=255, default='')

  # shooting stats
  sh = models.IntegerField(default=0)
  sot	= models.IntegerField(default=0)
  dist = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True)
  fk = models.IntegerField(default=0)
  pkscored = models.IntegerField(default=0)
  pkatt = models.IntegerField(default=0)

  # defending stats
  tkl = models.IntegerField(default=0)
  tklw = models.IntegerField(default=0)
  tklvsdrb = models.IntegerField(default=0)
  attvsdrb = models.IntegerField(default=0)
  press	= models.IntegerField(default=0)
  succ = models.IntegerField(default=0)
  blocks = models.IntegerField(default=0)
  inter = models.IntegerField(default=0)
  err = models.IntegerField(default=0)

  # passing stats
  pass_cmp = models.IntegerField(default=0)
  pass_att = models.IntegerField(default=0)
  pass_totdist = models.IntegerField(default=0)
  pass_prgdist = models.IntegerField(default=0)

  # playmaking stats
  sca = models.IntegerField(default=0)
  sca_passlive = models.IntegerField(default=0)
  sca_passdead = models.IntegerField(default=0)
  sca_drib = models.IntegerField(default=0)
  sca_sh = models.IntegerField(default=0)
  sca_fld = models.IntegerField(default=0)
  sca_def = models.IntegerField(default=0)
  gca = models.IntegerField(default=0)
  gca_passlive = models.IntegerField(default=0)
  gca_passdead = models.IntegerField(default=0)
  gca_drib = models.IntegerField(default=0)
  gca_sh = models.IntegerField(default=0)
  gca_fld = models.IntegerField(default=0)
  gca_def = models.IntegerField(default=0)

  # possession stats
  touches = models.IntegerField(default=0)
  touches_defthird = models.IntegerField(default=0)
  touches_attpen = models.IntegerField(default=0)
  touches_attthird= models.IntegerField(default=0)
  carries = models.IntegerField(default=0)
  carries_totdist = models.IntegerField(default=0)
  carries_prgdist = models.IntegerField(default=0)
  progcarries = models.IntegerField(default=0)
  progpassrec = models.IntegerField(default=0)

  # gk stats
  sota = models.IntegerField(null=True, blank=True)
  saves = models.IntegerField(null=True, blank=True)
  psxg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, default=0)
  psxg_pm = models.DecimalField(max_digits=6, decimal_places=2,null=True, blank=True, default=0)

  # misc stats
  crdy = models.IntegerField(default=0)
  crdr = models.IntegerField(default=0)
  twocrdy = models.IntegerField(default=0)
  fls = models.IntegerField(default=0)
  fld = models.IntegerField(default=0)
  off = models.IntegerField(default=0)
  recov = models.IntegerField(default=0)
  arlwon = models.IntegerField(default=0)
  arllost = models.IntegerField(default=0)

  class Meta:
    abstract = True

class MatchStat(Stat):
  match_id = models.CharField(max_length=255, primary_key=True)
  date = models.DateField()
  time = models.TimeField()
  comp = models.CharField(max_length=255)
  gameweek = models.CharField(max_length=255)
  day = models.CharField(max_length=255)
  venue = models.CharField(max_length=255)
  result = models.CharField(max_length=255)
  gf = models.IntegerField(default=0)
  ga = models.IntegerField(default=0)
  opponent = models.CharField(max_length=255)
  xg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
  xga = models.DecimalField(max_digits=6, decimal_places=2, default=0)
  poss = models.IntegerField(default=0)
  attendance = models.IntegerField(default=0)
  captain = models.CharField(max_length=255)
  formation = models.CharField(max_length=255)
  referee =  models.CharField(max_length=255)

class PlayerStat(Stat):
  player_team = models.CharField(max_length=255, primary_key=True)
  player = models.CharField(max_length=255)
  nation = models.CharField(max_length=255)
  pos = models.CharField(max_length=255)
  age = models.IntegerField(default=0)
  mp = models.IntegerField(default=0)
  starts = models.IntegerField(default=0)
  minutes = models.IntegerField(default=0)
  ninetys = models.DecimalField(max_digits=6, decimal_places=2, default=0)
  gls = models.IntegerField(default=0)
  ast = models.IntegerField(default=0)
  npg = models.IntegerField(default=0)
  xg = models.DecimalField(max_digits=6, decimal_places=2,)
  npxg = models.DecimalField(max_digits=6, decimal_places=2,)
  xa = models.DecimalField(max_digits=6, decimal_places=2,)
  np_xgoal_contrib = models.DecimalField(max_digits=6, decimal_places=2, default=0)
