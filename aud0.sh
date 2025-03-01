# weaves
#
d_set () {
  ${FUNCNAME#d_} 
}

## transmission client

h_ls () {

  cat <<EOF


EOF

}

d_ls () {
  local e_cmd=$1
  shift

  case $e_cmd in
    counted)
      : ${d_dir:=$PWD}
      local tfile=$(mktemp)
      f_tpush $tfile

      awk -v ddir="$d_dir" 'BEGIN { ctr=1 } length($0) { tag=$0; gsub(/.*\./, "", tag); printf("%s/%03d-file.%s\n", ddir, ctr, tag); ctr+=1 }' 

      ;;

  esac
}

