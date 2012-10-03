#!/bin/bash

# atualiza tag "release" para apontar para a revisao corrente
git tag -d release && git push origin :release && git tag release && git push && git push --tags
