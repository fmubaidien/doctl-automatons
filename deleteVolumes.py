import subprocess as sp

pc = sp.Popen(["doctl", "compute", "volume", "list","--no-header", "--format",  "ID,Name,DropletIDs"], stdout=sp.PIPE)
data = pc.stdout.read().decode("utf-8")

data = data.split("\n") #split data into rows

clean = [] #store data as 2D array
for row in data:
    clean.append(row.split("   ")) #split based on 3 spaces since the tab is 3 spaces
clean.pop(-1) #an extra unnecessary row is added at the end so this is to get rid of it

#print(clean[0][-1])


# for row in clean:
#     print(row)
#     for col in row:
#         col = col.replace(" ","")

# print(clean[0][-1])
count=0
for row in clean:
    if row[-1]==" ":
        print(row)
        if "pvc" in row[1]: #Check if the volume is a kuberenetes volume
            print("deleting", row[1])
            sp.run(["doctl", "compute", "volume", "delete", row[0]], capture_output=True, text=True, input="y")
            print(row[1], "deleted successfully")
            count+=1
        else:
            x = input("You are about to delete ",row[1], " are you sure you wish to continue? [y/n]")
            if x=='y' or x=="Y" or x=="YES" or x=="yes":
                sp.run(["doctl", "compute", "volume", "delete", row[0]], capture_output=True, text=True, input="y")
                count+=1

print(count, "Volumes have been deleted successfully")
