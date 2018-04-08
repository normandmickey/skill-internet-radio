# The requirements.sh is an advanced mechanism and should rarely be needed.
# Be aware that it won't run with root permissions and 'sudo' won't work
# in most cases.

#detect distribution using lsb_release (may be replaced parsing /etc/*release)
dist=$(lsb_release -d |awk '{print$2}')

dependencies=( vlc )

#setting dependencies and package manager in relation to the distribution
if [ "$dist"  == "Arch"  ]; then
    pm="pacman -S"
elif [ "$dist" ==  "Ubuntu" ] || [ "$dist" == "KDE" ] || [ "$dist" == "Debian" ]; then
    pm="apt install"
elif [ "$dist" == "Raspbian" ]; then
    # Can't do 'sudo' with standard MSM install on a Mark 1 or Picroft,
    # use pkcon instead which doesn't need sudo
    for dep in "${dependencies[@]}"
    do
        pkcon install $dep
    done
    exit 0
fi


# installing dependencies
for dep in "${dependencies[@]}"
do
    sudo $pm $dep
done

exit 0