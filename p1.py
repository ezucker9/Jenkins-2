# "ADD YOUR CODE HERE"
def create_cust_dictionary(balancefile):

    file=open(balancefile+".txt",'r')
    cdictionary=dict()

    for line in file.readlines(): 
        t=line.split()
        cdictionary[t[0]]=[t[1],t[2],0,0]
    file.close()
   
    return cdictionary

def update_cust_dictionary(cdictionary,transfile):

    file=open(transfile+".txt",'r')
    

    for line in file.readlines(): 

        t=line.split()
        exists=t[0] in cdictionary

        if exists :
            value=float(t[1])

            if value > 0:
                deposit=float(cdictionary[t[0]][2])
                cdictionary[t[0]][2]=deposit+value
            else :
                withdraw=abs(float(cdictionary[t[0]][3]))
                cdictionary[t[0]][3]=withdraw+abs(value)
    file.close()

    
def process_transactions(oldbalfile,transfile,transummfile,newbalfile):

    cdictionary=create_cust_dictionary(oldbalfile)
    update_cust_dictionary(cdictionary,transfile)

    ord_dic = dict(sorted(cdictionary.items()))

    with open(transummfile+".txt", "w") as trans , open(newbalfile+".txt", "w") as bal:

        trans.write('{:<8} {:<11} {:>10} {:>10} {:>12}  {:>8}  {:>8}  {:>9}'.format('ACCOUNT#','SSN','PREV BAL','DEPOSITS','WITHDRAWALS','INTEREST','PENALTY','NEW BAL'))
        trans.write('\n--------------------------------------------------------------------------------------\n')
        bal.write('{:<8} {:<11} {:>10} '.format('ACCOUNT#','SSN','BALANCE'))
        bal.write('\n------------------------------\n')

        for key, value  in ord_dic.items():
            number=key
            ssn=value[1]
            prev_bal=float(value[1])
            deposits=float(value[2])
            withdrawals=float(value[3])
            penalty=0
            interest=0
            if (prev_bal+deposits-withdrawals) > 3000:
                interest=(prev_bal+deposits-withdrawals)*2/100
                penalty=0
            elif (prev_bal+deposits-withdrawals) < 100:
                interest=0
                penalty=10.00
            new_balance=(prev_bal+deposits-withdrawals)+interest-penalty

            trans.write('{:<8} {:<11} {:>10,.2f} {:>10,.2f} {:>12.2f}  {:>8.2f}  {:>8.2f}  {:>9.2f}\n'.format(number, ssn,prev_bal,deposits, withdrawals,interest,penalty,new_balance))
            bal.write('{:<8} {:<11} {:>10,.2f}\n'.format(number, ssn,new_balance))
    
    trans.close()
    bal.close()


    
# # main 
process_transactions("balance.dat", "transactions.dat", 
                                     "transsummary.dat", "newbalance.dat")


