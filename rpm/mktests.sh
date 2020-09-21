#!/bin/sh

cat <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<testdefinition version="1.0">
    <suite name="libnice-tests">
        <description>Libnice tests</description>
        <set name="libnice-unit-tests">
EOF

for testcase in $(cat tests/libnice-tests.list)
do
    testcase_name=$(echo $testcase|sed 's/\//_/')
    attributes="name=\"$testcase_name\""
    insignificant=`grep "^$testcase" tests/INSIGNIFICANT || true`
    if test -n "$insignificant"
    then
        continue
        attributes="$attributes insignificant=\"true\""
    fi
    cat <<EOF
            <case $attributes>
                <step>/opt/tests/libnice/bin/$testcase</step>
            </case>
EOF
done

cat <<EOF
            <case name="test-pseudotcp-random">
                <step>dd if=/dev/urandom of=/tmp/rand count=1024 ibs=1024</step>
                <step>/opt/tests/libnice/bin/nice-test-pseudotcp /tmp/rand /tmp/rand.copy</step>
                <step>diff /tmp/rand /tmp/rand.copy</step>
                <step>rm /tmp/rand /tmp/rand.copy</step>
            </case>
        </set>
    </suite>
</testdefinition>
EOF
