build_tree="${up_path}/build/cado-nfs-build"
PREFIX=/usr/local
CFLAGS="-O3 -DNDEBUG -march=native"
CXXFLAGS="$CFLAGS"
BWC_GF2_ARITHMETIC_BACKENDS="m128;u64k1"
BWC_GFP_ARITHMETIC_BACKENDS=""
ENABLE_SHARED=1
