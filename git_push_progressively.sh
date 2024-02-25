#!/bin/bash

# Vérifiez si le message de commit est passé en argument
if [ $# -eq 0 ]; then
    echo "Veuillez fournir un message de commit en argument."
    exit 1
fi

commit_message=$1

while true; do
    # Obtenez une liste des fichiers modifiés
    IFS=$'\n'
    files=($(git status --porcelain | awk 'BEGIN{srand()} {print rand() "\t" $0}' | sort -n | cut -f2-))

    # Vérifiez si la liste de fichiers est vide
    if [ ${#files[@]} -eq 0 ]; then
        echo "Aucun fichier à ajouter. Fin du script."
        break
    fi

    # Ajoutez les fichiers à l'index de git
    for file in "${files[@]}"; do
        status=$(echo "$file" | awk '{print $1}')
        file_path=$(echo "$file" | awk '{print substr($0, index($0,$2))}')
        if [ -n "$file_path" ]; then
            if [ "$status" == "D" ]; then
                git rm --cached "$file_path"
            else
                git add "$file_path"
            fi
        fi
    done

    # Commit et push
    git commit -m "$commit_message"
    git push
done