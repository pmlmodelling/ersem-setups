program make_forcing

  implicit none
  integer :: i,t
  integer,parameter :: mgl=7,ngl=6
  real,dimension(mgl):: short_wave,net_heat
  real :: short_wave0,net_heat0
  real,dimension(ngl):: u10,v10
  real :: day,hour,solar,net,u,v,time
  real,parameter :: pi = 3.1415926
  integer :: year0,month0,day0
  integer :: year,month,day1,hour1
  integer :: timet
  open(1,file='~/data01/changjiang_biology/water_quality/CE_QUAL_ICM/make_forcing/SWR_2015.dat',status='old')
  open(2,file='~/data01/changjiang_biology/water_quality/CE_QUAL_ICM/make_forcing/wind_2015.dat',status='old')

  open(3,file='1D_wnd.dat',form='unformatted',status='replace')
  open(4,file='1D_hfx.dat',form='unformatted',status='replace')
 
  year0=2005
  month0=1
  day0=1

  do t=1,2920
     !read(1,*)day,hour,solar,net
     !short_wave = solar
     !net_heat = net

     ! Analytical solution
     short_wave=50.0+450.0+450.0*sin((t-1-2920/4.0)/(2920/4.0)*pi/2.0)
     net_heat = 140.0*sin((t-1-2920/8.0)/(2920/4.0)*pi/2.0)

     ! historical ecwmf forcing 
     !read(1,*)day,hour,short_wave0,net_heat0
     !short_wave =short_wave0
     !net_heat = net_heat0

     read(2,*)day,hour,u,v
     u10=u
     v10=v
     if(t==1)then
        time=0.0
     elseif(t==2920)then
        time=(day+1)*24
     else
        time=day*24+hour
     end if
     call caldate(int(time)*3600,year,month,day1,hour1,year0,month0,day0)
     if(hour1>18.or.hour1<6)short_wave=0.0
     write(3)time
     write(4)time
     write(3)(u10(i),v10(i),i=1,ngl)
     write(4)(net_heat(i),short_wave(i),i=1,mgl)
     !print*,year,month,day1,hour1
     print*,time,net_heat(1),short_wave(1),hour1
  end do

  close(1)
  close(2)
  close(3)
  close(4)

end program make_forcing


subroutine caldate(timet,year,month,day,hour,year0,month0,day0)
INTEGER,INTENT(IN) :: timet,year0,month0,day0
INTEGER,INTENT(OUT):: year,month,day,hour
hour = timet/3600.
day = day0 + int(hour/24)
hour = hour - 24*int(hour/24)
month = month0
year = year0
10  continue
if(month.eq.1 .or. month.eq. 3 .or. month.eq.5 .or. month.eq.7 .or. month.eq.8 .or. month.eq.10 .or. month.eq.12) then
   if(day.gt.31) then
      month = month + 1
      if(month.eq.13) then
         month = 1
         year = year+1
      endif
      day = day - 31
    else
    goto 20
   endif
elseif(month.eq.2) then
   if(mod(int(year),4).eq.0) then
      if(day.gt.29) then
         month = month +1
         day = day - 29
      else
         goto 20
      endif
   else
      if(day.gt.28) then
         month = month +1
         day = day - 28
      else
         goto 20
      endif
   endif
else
   if(day.gt.30) then
      month = month +1
      day = day - 30
   else
      goto 20
   endif
endif
goto 10
20  continue

return
end subroutine caldate
