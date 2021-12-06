# Imports
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from scipy import integrate
import numpy as np
import cmath as cm
import time


# Conditions
epo = 8.85418782 * 10**(-12) # m^-3 kg^-1 s^4 A^2
c = 299792458 # m/s
wavelength = 10**(-6) # m
k = (2*np.pi)/wavelength # m^-1
Eo = 1
pi = np.pi
z = 0.02
xapwidth = 10**-5
yapwidth = 10**-5
apN = 100

# Screen positions used to different to adjust independently for loading times
screenmin = -5*10**(-3)
screenmax = 5*10**(-3)
screenspace = (screenmax - screenmin)/1000

xscreenmin = -5*10**(-3)
xscreenmax = 5*10**(-3)
xscrN = 100
xscreenspace = (xscreenmax - xscreenmin)/xscrN


yscreenmin = -5*10**(-3)
yscreenmax = 5*10**(-3)
yscrN = 100
yscreenspace = (yscreenmax - yscreenmin)/yscrN



# Definitions

# 1D Integral Stuff
def func(xscreen, xaper, z):
    """Function we are integrating, cm.rect takes an amplitude (used 1) and the angle from the equation, this gives
    a complex number for an inputted screen and aperture position"""

    expo = cm.rect(1, ((k / (2 * z)) * ((xscreen - xaper) ** 2)))

    coef = (k * Eo) / (2 * (pi) * z)

    functionvalue = coef * expo

    return functionvalue


def simpson(b, apwidth):
    """Generalised simpson integral method, screen distance and aperture width are inputted, this creates arrays for
    screen values and aperture values across then integrates them (ie takes screen position, say -5mm, then integrates
    across the aperture, then uses -4.99mm and so on"""

    apspace = (apwidth * 10 ** -2)
    xap2 = apwidth
    xap1 = -apwidth

    x1range = np.arange(xap1, xap2 + (apspace / 2), apspace)
    xrange = np.arange(screenmin, screenmax + (screenspace / 2), screenspace)

    x1numstrips = len(x1range)
    xnumstrips = len(xrange)

    simpcoef = np.zeros(x1numstrips, dtype="complex")

    simpcoef[1::2] = 4
    simpcoef[2::2] = 2
    simpcoef[0] = 1
    simpcoef[x1numstrips - 1] = 1

    AreaArray = np.zeros(x1numstrips, dtype="complex")

    xAreaValue = np.zeros(xnumstrips, dtype="complex")

    for r in range(xnumstrips):

        m = xrange[r]

        for i in range(x1numstrips):
            AreaArray[i] = func(m, x1range[i], b)

        xAreaValue[r] = ((apspace / 3) * np.sum(simpcoef * AreaArray))

    compE = xAreaValue

    I = epo * c * np.abs(compE)

    return I, xrange


def plot():
    """Creates singular plot function for convenience in the menu system, the
    functionality of the sliders and buttons depend on the python editor
    settings (built in pycharm with needed modules imported)"""

    # Sets y and x range for integral using simpson function above
    yvals = simpson(2 * 10 ** (-2), 10 ** -5)[0]
    xvals = 1000 * simpson(2 * 10 ** (-2), 10 ** -5)[1]

    # Sets plot
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.subplots_adjust(left=0.1, bottom=0.4)
    plt.xlabel('Screen Coordinate (mm)')
    plt.ylabel('Intensity')
    plt.title('Intensity across screen')
    p, = plt.plot(xvals, yvals, linewidth=2, color='red')

    # Slider to adjust screen distance
    zslider1 = plt.axes([0.2, 0.28, 0.6, 0.03])
    zslider = Slider(zslider1, 'Screen Distance (cm)', valmin=0.2, valmax=10, valstep=0.2, valinit=2, valfmt='%1.1f')
    zbutton1 = plt.axes([0.88, 0.28, 0.07, 0.03])
    zbutton = Button(zbutton1, 'z Reset')

    # Slider to change aperture
    apslider1 = plt.axes([0.2, 0.2, 0.6, 0.03])
    apslider = Slider(apslider1, 'Aperture (10^(-7) m )', valmin=0.1, valmax=1000, valstep=10, valinit=100,
                      valfmt='%0.0f')
    apbutton1 = plt.axes([0.86, 0.2, 0.12, 0.03])
    apbutton = Button(apbutton1, 'Aperture Reset')

    warning1 = plt.axes([0.2, 0.05, 0.40, 0.1])
    warningbutton = Button(warning1, 'The functionality of the sliders and buttons depends\n on the python editor settings\n (built in pycharm with needed modules imported)')

    # Resets both parameters
    allbutton1 = plt.axes([0.88, 0.12, 0.07, 0.03])
    allbutton = Button(allbutton1, 'Reset All')

    # z slider update and reset
    def zupdate(val):
        """re-calculates and plots the graph under the parameter set in the slider for the adjustment of screen
        distance, configuring the axis for this as well"""
        yvals = simpson(zslider.val * (10 ** (-2)), apslider.val * (10 ** -7))[0]
        p.set_ydata(yvals)
        ax.clear()
        ax.plot(xvals, yvals, linewidth=2, color='red')

    # Reset Buttons
    def zreset(val):
        """updates the screen distance to the original of 2cm when pressed"""
        zslider.set_val(2)

    def apreset(val):
        """updates the aperture to the original of 10^-5m when pressed"""
        apslider.set_val(100)

    def allreset(val):
        """resets both variable parameters for convenience"""
        zslider.set_val(2)
        apslider.set_val(100)

    # Detects change in slider or button press

    # Screen Distance change detectors
    zslider.on_changed(zupdate)
    zbutton.on_clicked(zreset)

    # Aperture change detectors
    apslider.on_changed(zupdate)
    apbutton.on_clicked(apreset)

    allbutton.on_clicked(allreset)

    plt.show()




#2D integral Stuff
def colfunc(screen,aper, z):
    """Function we are integrating, cm.rect takes an amplitude (used 1) and the angle from the equation, this gives
    a complex number for an inputted screen and aperture position, amplitude taken out so we don't end with it
    squared for part C"""

    expo = cm.rect(1, ((k / (2 * z)) * ((screen - aper)**2)))



    functionvalue = expo


    return functionvalue


def colour():
    """Creates arrays for the 2d integration then plots them on a colour chart"""

    # E field at each pixel array
    Epix = np.zeros((yscrN, xscrN), dtype="complex")


    # x and y screen positions
    xscreen = np.linspace(xscreenmin, xscreenmax, xscrN)
    yscreen = np.linspace(yscreenmin, yscreenmax, yscrN)


    # Sets x and y aperture boundary conditions
    apspace = xapwidth*10**(-2)
    xap2 = xapwidth
    xap1 = -xapwidth

    yap2 = yapwidth
    yap1 = -yapwidth

    # Arrays for aperture directions
    xaprange = np.linspace(xap1, xap2 + (apspace/2), apN)
    yaprange = np.linspace(yap1, yap2 + (apspace/2), apN)


    # Added here, so it's only multiplied once
    coef = (k * Eo) / (2 * (pi) * z)


    # Creates range for every x across screen
    for x in range(len(xscreen)):

        xconst = xscreen[x]


        # Creates range for every y across screen
        for y in range(len(yscreen)):

            yconst = yscreen[y]

            # Used for building area arrays
            xArea = np.zeros(len(xaprange), dtype="complex")
            yArea = np.zeros(len(xaprange), dtype="complex")

            # Used to integrate across positions
            for s in range(len(xaprange)):

                xArea[s] = colfunc(xconst, xaprange[s], z)
                yArea[s] = colfunc(yconst, yaprange[s], z)


            Epix[x, y] = coef * np.sum(integrate.simps(xArea, xaprange, apspace) * integrate.simps(yArea, yaprange, apspace))



    IntensePix = c * epo * np.abs(Epix)


    colourplot = plt.imshow(IntensePix, extent=[-5, 5, -5, 5])
    plt.xlabel('x Coordinate (mm)')
    plt.ylabel('y Coordinate (mm)')
    plt.title('Colour scale image for Square Aperture')
    plt.colorbar()
    plt.show()


print("Hello, welcome to my program\n")
loop = 5
while loop<6:
    print("Please select an option\na) 1D Diffraction\nb) 2D Diffraction (Square Aperture)\nq) Quit Program")
    response = input()
    print()

    if response == 'a':
        aloop = 4
        while aloop<5:
            print("You have selected 1D integral\nPreparing Graph")
            plot()


            print()
            option = input('Please select an option\nc - Rerun 1D plot\nr - Main Menu\n')
            print()

            if option == 'r':
                break

            elif option == 'c':
                pass


            else:
                print('I will return you to the menu\n\n')
                time.sleep(0.5)
                break

    elif response == 'b':
        bloop = 5
        while bloop<6:
            print("You have selected 2D integral\nPreparing Plot")
            colour()


            print()
            option = input('Please select an option\nc - Rerun 2D plot\nr - Main Menu\n')
            print()

            if option == 'r':
                break

            elif option == 'c':
                pass

            else:
                print('I will return you to the menu\n\n')
                time.sleep(0.5)
                break

    elif response == 'q':
        print('Initiating Self Destruct...')
        time.sleep(0.5)
        print('Self Destructing in 5...')
        for i in range(5):
            time.sleep(1)
            print(4-i)
        print()
        print('BOOM!')
        break


    else:
        print('I will assume you made a mistake\n\n')
        time.sleep(1)