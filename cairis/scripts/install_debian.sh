#!/bin/bash
#

# Fixed values
CAIRIS_GIT='https://github.com/failys/CAIRIS.git'
APTDEP="python-dev build-essential mysql-server mysql-client graphviz docbook dblatex python-pip git libmysqlclient-dev --no-install-recommends texlive-latex-extra"
PYTHONDEP="mysql-python==1.2.3 pyparsing==1.5.7 pydot"
# Global variables
INSTALL_DESKTOP='x'
CAIRIS_USER=$USER
CAIRIS_DIR=/opt/cairis
DBNO="0"
PRECMD=""
DDBHOST=""
DDBPORT=""
DDBNAME=""
DDBUSER=""
DDBPASS=""

function check_sudo() {
	if [ "$EUID" -ne 0 ]; then
		sudo_path=$(which sudo)
		if [ "$sudo_path" == "" ]; then
			echo "sudo binary not found. Please install the sudo binary or run this script as root"
			exit
		fi

		$sudo_path -n true 2>/dev/null
		if [ "$?" -ne "0" ]; then
			echo "Please provide your password for root privileges"
			$sudo_path true
			if [ "$?" -ne "0" ]; then
				echo "Root privileges are required to install CAIRIS"
				echo "The installer will now exit..."
				exit 1
			fi
		fi
		PRECMD=$sudo_path
	else
		cat <<EOM

WARNING! Running this script using sudo or as root will make CAIRIS
only runnable under root. If this is not your intention, then
hit Ctrl+C and re-run the script as the user who will be running CAIRIS 
and without using the 'sudo' command.

Press any key to continue either way...
EOM
	read C_VOID
	fi
}

function install_sys_dep() {
	cat <<EOM

##############################################
# Installing system dependencies             #
##############################################

EOM
	if [ "$INSTALL_DESKTOP" == "y" ]
	then
		APTDEP="python-wxglade python-glade2 python-wxgtk2.8 "$APTDEP
	fi

	$PRECMD apt-get install $APTDEP

	if [ "$?" -ne "0" ]
	then
		cat <<EOM
An error occurred while installing the system dependencies for CAIRIS.
Please consult the apt-get log to resolve the issue. 
EOM
		exit 1
	else
		echo -e "System dependencies successfully installed\n"
	fi
}

function install_python_dep() {
	cat <<EOM

##############################################
# Installing Python dependencies             #
##############################################

EOM
	$PRECMD pip install $PYTHONDEP

	if [ "$?" -ne "0" ]
	then
		echo "An error occurred while installing the Python dependencies for CAIRIS."
		echo "Please consult the pip log to resolve the issue"
		exit 1
	else
		echo -e "Python dependencies successfully installed\n"
	fi
}

function create_user() {
	cat <<EOM

##############################################
# Security                                   #
##############################################

To ensure proper functioning, it is advised that CAIRIS is run 
by a specific system user or a user that belongs to a specific group. 

The installer can create this user and group, and can make 
the current user a member of this group.

EOM

	cu=""
	while [ "$cu" != "y" -a "$cu" != "n" ]; do
		echo "Would you like the installer to do this? [Y/n]"
		read cu
		if [ "$cu" == "" ]; then cu="y"; fi
		cu=${cu,,}
		if [ "$cu" != "y" -a "$cu" != "n" ]; then echo -e "Invalid input\n"; fi
	done

	if [ "$cu" == "y" ]
	then
		echo ""
		CAIRIS_USER='cairis'
		existing_cu=$($PRECMD cat /etc/passwd | grep -c "$CAIRIS_USER")
		if [ "$?" == "0" -a "$existing_cu" -gt "0" ]; then
			echo -e "User already exists (that's good)"
		else
			$PRECMD useradd --no-create-home --system $CAIRIS_USER
			if [ "$?" -ne "0" ]; then echo "CAIRIS encountered an error. Exiting..."; exit 1; fi
		fi
		$PRECMD usermod -a -G $CAIRIS_USER "$USER"
		if [ "$?" -ne "0" ]; then 
			echo "CAIRIS encountered an error. Please check your user's groups after installation."
		else
			echo "Current user was successfully added to group '$CAIRIS_USER'"
		fi
	fi	
}

function download_cairis() {
	cat <<EOM

##############################################
# Downloading CAIRIS                         #
##############################################

Where do you want to install CAIRIS? [/opt/cairis]
EOM
	read CAIRIS_DIR
	if [ "$CAIRIS_DIR" == "" ]
	then
		CAIRIS_DIR=/opt/cairis
	else
		i=$((${#CAIRIS_DIR}-1))
		last_letter=${CAIRIS_DIR:$i:1}
		if [ "$last_letter" == "/" ]; then CAIRIS_DIR=${CAIRIS_DIR:0:$i}; fi
	fi
	if [ -d "$CAIRIS_DIR" ]; then
		cat <<EOM 
The provided target directory is not empty.
Git requires the target directory to be empty.
Please resolve this before running the installer again, 
or choose another location to install CAIRIS.

Exiting...

EOM
		exit 1
	fi

	$PRECMD git clone $CAIRIS_GIT $CAIRIS_DIR
	if [ "$?" -ne "0" ]; then
		echo "Error retrieving source code for CAIRIS. Please check the above error message."
		exit 1
	fi
	$PRECMD chown -R $CAIRIS_USER:$CAIRIS_USER $CAIRIS_DIR
	$PRECMD chmod -R 775 $CAIRIS_DIR
	if [ "$?" -ne "0" ]; then
		echo "Error while setting up CAIRIS application directory. Exiting..."
		exit 1
	fi
}

function developer_branch() {
	cat <<EOM

##############################################
# Experimental branch                        #
##############################################

Certain features may not be implemented in the master branch yet.
If you want, you can switch to the develop branch, which contains experimental code.

Do you want to switch to this branch? [y/N]
EOM
	bsw=""
	while [ "$bsw" != "y" -a "$bsw" != "n" ]
	do
		read bsw
		if [ "$bsw" == "" ]; then bsw="n"; fi
		bsw=${bsw,,}
		if [ "$bsw" != "y" -a "$bsw" != "n" ]; then echo -e "Invalid input\n\nWould you like the installer to do this? [Y/n]\n"; fi
	done

	if [ "$bsw" == "y" ]; then
		cd $CAIRIS_DIR
		git checkout develop
	fi
}

function create_db() {
	echo -ne "\nDatabase host [127.0.0.1]: "
	read dbhost
	if [ "$dbhost" == "" ]; then dbhost="127.0.0.1"; fi

	echo -ne "Database port [3306]: "
	read dbport
	if [ "$dbport" == "" ]; then dbport="3306"; fi

	echo -ne "Database name [cairis]: "
	read dbname
	if [ "$dbname" == "" ]; then dbname="cairis"; fi

	echo -ne "Database user [cairis]: "
	read dbuser
	if [ "$dbuser" == "" ]; then dbuser="cairis"; fi

	echo -ne "Database password [cairis123]: "
	stty_orig=$(stty -g)
	stty -echo
	read dbpass
	if [ "$dbpass" == "" ]; then dbpass="cairis123"; fi
	stty "$stty_orig"

	echo -e "\nPlease provide the MySQL root password when asked."
	mysql -u root -p -h "$dbhost" << EOF
GRANT USAGE ON *.* TO '$dbuser'@'$dbhost' IDENTIFIED BY '$dbpass' 
WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0
MAX_USER_CONNECTIONS 0;
CREATE DATABASE IF NOT EXISTS \`$dbname\`;
GRANT ALL PRIVILEGES ON \`$dbname\`.* TO '$dbuser'@'$dbhost';
EOF
	if [ "$?" != "0" ]; then echo -e "\nProblem creating the database.\nExiting..."; return; fi
	mysql -u "$dbuser" --password="$dbpass" -h "$dbhost" --database="$dbname" < $CAIRIS_DIR/cairis/sql/procs.sql
	if [ "$?" != "0" ]; then echo -e "\nProblem installing stored procedures.\nExiting..."; return; fi
	mysql -u "$dbuser" --password="$dbpass" -h "$dbhost" --database="$dbname" < $CAIRIS_DIR/cairis/sql/init.sql
	if [ "$?" != "0" ]; then echo -e "\nProblem installing base tables and view.\nExiting..."; return; fi

	if [ "$DDBHOST" == "" ]; then db_opt="Y/n"; else db_opt="y/N"; fi
	set_db=""

	echo -e "\nDatabase successfully installed.\n"
	DBNO=$(($DBNO+1))
	
	while [ "$set_db" != "y" -a "$set_db" != "n" ]; do
		echo "Do you want CAIRIS to use this database connection as default connection? [$db_opt]"
		read set_db
		if [ "$set_db" == "" ]; then if [ "$DDBHOST" == "" ]; then set_db="y"; else set_db="n"; fi; fi
		set_db=${set_db,,}
		if [ "$set_db" != "y" -a "$set_db" != "n" ]; then echo -e "Invalid input\n"; fi
	done

	if [ "$set_db" == "y" ]; then
		DDBHOST=$dbhost
		DDBPORT=$dbport
		DDBNAME=$dbname
		DDBUSER=$dbuser
		DDBPASS=$dbpass
	fi
}

function db_install() {
	cat <<EOM

##############################################
# Database installation                      #
##############################################

The installer can install the base tables, views and
stored procedures which are required for a CAIRIS database instance.

EOM
	dbc=""
	while [ "$dbc" != "y" -a "$dbc" != "n" ]; do
		echo "Do you want the installer to do this now? [Y/n]"
		if [ "$dbc" == "" ]; then dbc="y"; fi
		dbc=${dbc,,}
		if [ "$dbc" != "y" -a "$dbc" != "n" ]; then echo -e "Invalid input\n"; fi
		if [ "$dbc" == "n" ]; then DBNO=$(($DBNO+1)); fi
	done
	while [ "$dbc" == "y" ]; do
		create_db
		dbc=""
		while [ "$dbc" != "y" -a "$dbc" != "n" ]; do
			echo -e "\nDo you want to prepare another database instance? [y/N]"
			if [ "$dbc" == "" ]; then dbc="n"; fi
			dbc=${dbc,,}
			if [ "$dbc" != "y" -a "$dbc" != "n" ]; then echo -e "Invalid input\n"; fi
		done
	done
	if [ "$DBNO" == "0" ]; then cat <<EOM

Database creation failed. 

Make sure that you have at least one working database instance before you continue.
EOM
	fi
}

function conf_setup() {	
	cat <<EOM

##############################################
# CAIRIS configuration                       #
##############################################

CAIRIS needs to be configured before it is able run.
The installer can help creating a configuration file.
You can later still edit this file at the following location:

$HOME/CAIRIS/cairis/cairis/config/cairis.cnf

EOM
	co=""
	while [ "$co" != "y" -a "$co" != "n" ]; do
		echo "Do you want to configure CAIRIS now? [Y/n]"
		read co
		if [ "$co" == "" ]; then co="y"; fi
		co=${co,,}
		if [ "$co" != "y" -a "$co" != "n" ]; then echo -e "Invalid input\n"; fi
	done
	config_dir="$HOME/CAIRIS/cairis/config"
	mkdir -p -m 700 "$config_dir"
	cp "$CAIRIS_DIR/cairis/config/cairis.cnf" "$config_dir/"
	chmod 600 "$config_dir/cairis.cnf"
	if [ "$co" == "y" ]; then
		mysql -u "$DDBUSER" --password="$DDBPASS" -h "$DDBHOST" --database="$DDBNAME" -e "SHOW TABLES" > /dev/null 2>&1
		test=$?
		while [ "$test" != "0" ]; do
			echo -e "\nPlease provide the proper credentials for an existing CAIRIS database"
			echo -n "Host: "
			read DDBHOST
			echo -n "Port: "
			read DDBPORT
			echo -n "Database name: "
			read DDBNAME
			echo -n "Database user: "
			read DDBUSER
			echo -n "Database password: "
			stty_orig=$(stty -g)
			stty -echo
			read DDBPASS
			stty "$stty_orig"
			mysql -u "$DDBUSER" --password="$DDBPASS" -h "$DDBHOST" --database="$DDBNAME" -e "SHOW TABLES" > /dev/null 2>&1
			test=$?
			if [ "$test" != "0" ]; then 
				echo -e "Invalid credentials. No access allowed...\n"
			else
				echo " "
			fi
		done
			
		sed -i -e 's|dbhost = |dbhost = '"$DDBHOST"'|g' "$config_dir/cairis.cnf"
		sed -i -e 's|dbport = |dbport = '"$DDBPORT"'|g' "$config_dir/cairis.cnf"
		sed -i -e 's|dbuser = |dbuser = '"$DDBUSER"'|g' "$config_dir/cairis.cnf"
		sed -i -e 's|dbpasswd = |dbpasswd = '"$DDBPASS"'|g' "$config_dir/cairis.cnf"
		sed -i -e 's|dbname = |dbname = '"$DDBNAME"'|g' "$config_dir/cairis.cnf"
		sed -i -e 's|root = |root = '"$CAIRIS_DIR/cairis"'|g' "$config_dir/cairis.cnf"
		
		web_port="0"
		echo -e "\nCAIRIS can run on any web port as long as it is available.\n"
		while [ "$web_port" -lt "1" -o "$web_port" -gt "65536" ]; do
			echo "Which port would you like CAIRIS to run on? [7071]"
			read web_port
			if [ "$web_port" == "" ]; then web_port="7071"; fi
			if [ "$web_port" -lt "1" -a "$web_port" -gt "65536" ]; then echo -e "Invalid input\n"; fi
		done
		sed -i -e 's|web_port = |web_port = '"$web_port"'|g' "$config_dir/cairis.cnf"
		
		cat <<EOM

CAIRIS uses a predefined directory to store uploaded content in.

Which directory do you want to use? [$HOME/CAIRIS/uploads]
EOM
		read upload_dir
		if [ "$upload_dir" == "" ]; then upload_dir="$HOME/CAIRIS/uploads"; fi
		if ! [ -d "$web_dir" ]; then cat <<EOM 

The provided directory does not exist on the system.

Out of security reasons, the installer will not create the directory.
Make sure that the directory does exist and has the right permission
when running CAIRIS for the first time.

EOM
		fi
		sed -i -e 's|upload_dir = |upload_dir = '"$upload_dir"'|g' "$config_dir/cairis.cnf"
	fi
}

check_sudo

if [ "$1" == "" ]; then
	cat <<EOM

##############################################
# Desktop application                        #
##############################################

CAIRIS can also run as a desktop application. However this requires extra dependencies to be installed.

EOM
	while [ "$INSTALL_DESKTOP" != "y" -a "$INSTALL_DESKTOP" != "n" ]; do
		echo -e "Do you want to include the desktop application in the installation? [y/N]"
		read INSTALL_DESKTOP
		if [ "$INSTALL_DESKTOP" == "" ]; then INSTALL_DESKTOP="n"; fi
		INSTALL_DESKTOP=${INSTALL_DESKTOP,,}
		if [ "$INSTALL_DESKTOP" != "y" -a "$INSTALL_DESKTOP" != "n" ]; then
			echo -e "Invalid input\n"
		fi
	done

	install_sys_dep
	install_python_dep
	create_user
	download_cairis
	developer_branch
	db_install
	conf_setup

	cat <<EOM

##############################################
# Installation completed                     #
##############################################

CAIRIS was successfully installed.


To run CAIRIS in web mode, you can use the following command:

	python $CAIRIS_DIR/cairis/cairisd.py

To run it in desktop mode, use the following command:

	python $CAIRIS_DIR/cairis/cairis.py

You might first need to re-login in order for the 
group assignment to be applied to your session.


CAIRIS can also be operated via web interface.
To enable the web interface, please visit
https://github.com/RafVandelaer/Cairis-web-develop
and follow the instructions to install the web interface.

EOM
	exit 0
elif [ "$1" == "--config" -o "$1" == "-c" ]; then
	cat <<EOM

Please provide the path of the CAIRIS directory. 
(Normally this would be the directory which contains the cloned repository)

EOM
	echo "CAIRIS directory [/opt/cairis]: "
	read CAIRIS_DIR
	if [ "$CAIRIS_DIR" == "" ]; then CAIRIS_DIR=/opt/cairis; fi
	conf_setup
	exit 0
fi
