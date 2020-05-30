#!/bin/bash

######### Global Definitions ########
libName="GSL"
binName="gsl-config"
minVersion=2.5

######### Helper Functions ########

function check()
{
 if [ ! $? -eq 0 ]
 then
  exit $?
 fi 
}

# Help display function
function print_help ()
{
 echo ""
 echo "Syntax: ./install_${libName}.sh [--jobs=N] [--check]"
 echo ""
 echo "Where:"
 echo " --no-install If ${libName} is not found, do not download and install it."
 echo " --jobs=N Specifies N jobs to use when building ${libName}."
 echo " --help Displays this help message."
}

######### Environment Configuration ########

NJOBS=4
baseKoraliDir=$PWD
foundbinVersionFile=0
install=1

if [ -f $baseKoraliDir/docs/VERSION ]; then
 foundbinVersionFile=1
fi

if [ -f $baseKoraliDir/../docs/VERSION ]; then
 foundbinVersionFile=1
 baseKoraliDir=$PWD/../
fi

if [ $foundbinVersionFile == 0 ]; then
  echo "[Korali] Error: You need to run this file from Korali's base folder."
  exit 1
fi

######### Argument Parsing ########

for i in "$@"
do
case $i in
    --jobs=*)
    NJOBS="${i#*=}"
    shift
    ;;
    --no-install)
    install=0
    shift 
    ;;
    --help)
    print_help
    exit 0 
    shift 
    ;;
    *)
    print_help
    echo ""
    echo "[Korali] Error:  Unknown option $i."       
    exit 1
    ;;
esac
done

######## Checking for existing software ########

prereqsDir=${baseKoraliDir}/prereqs
baseLibDir=${prereqsDir}/${libName}
installDir=${baseLibDir}/install
buildDir=${baseLibDir}/build

binFound=0
binPath=${installDir}/bin/${binName}

if [ ! -f ${binPath} ]; then
 binPath=${binName}
fi

$binPath --version > /dev/null 2>&1
if [ $? -eq 0 ]; then
 binVersion=`${binPath} --version`
 cmpver=`printf "${binVersion}\n${minVersion}" | sort -V | head -n 1`
 
 if [[ "$cmpver" != "$minVersion" ]]; then
    echo "[Korali] ${libName} version found (${binVersion}) is smaller than required (${minVersion})."
 else
    binFound=1
    echo "[Korali] Found existing ${libName} version ${binVersion}. Skipping installation..."
 fi
fi

######## If not installed, download and install ########

if [ ${binFound} == 0 ]; then

 if [ ${install} == 0 ]; then
   echo "[Korali] Could not find an installation of ${libName}."
   exit 1
 fi
 
 
 echo "[Korali] Downloading ${libName}... "
 
 rm -rf $buildDir; check
 rm -rf $installDir; check
 
 mkdir -p $buildDir; check
 pushd $buildDir; check
 
 rm -f gsl-2.6.tar.gz; check
 rm -rf gsl-2.6; check
 
 wget 'ftp://ftp.gnu.org/gnu/gsl/gsl-2.6.tar.gz'; check
 tar -xzvf gsl-2.6.tar.gz ; check
  
 echo "[Korali] Configuring ${libName}... "
 cd gsl-2.6
 ./configure --prefix=$installDir; check
 
 echo "[Korali] Building ${libName}... "
 make -j$NJOBS; check
 
 echo "[Korali] Installing ${libName}... "
 make install; check
 
 popd; check
 
 echo "[Korali] Finished installing ${libName}."
 binPath=${installDir}/bin/${binName}
 
 echo "[Korali] Cleaning up build folder..."
 rm -rf $buildDir; check
fi

######## Finalization ########

fullBinPath=`which ${binPath}`
ln -sf $fullBinPath ${prereqsDir}/${binName}; check
binVersion=`${prereqsDir}/${binName} --version`; check 
echo "[Korali] Using ${libName} version $binVersion"

exit 0