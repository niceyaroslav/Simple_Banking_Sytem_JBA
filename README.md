# Simple BankingSytem JBA
<p>This is a project I have made while learning Python on the JetBrains Academy platform hyperskill.org.<br>
It represents a simple banking system with following functionality:
</p>
    <p>Initial menu:</p>
    <ls>
      <li>1. Create an account  - creates an entry in the database
      <li>2. Log into an account - requests an entry from the database
      <li>0. Exit - terminates
     </ls>
     <br>
     <br>
      <p>Secondary menu (displayed If user chose to log in):</p>
      <ls>
          <li>1. Balance - requests balance
          <li>2. Add income - increments balance by an amount specified
          <li>3. Do transfer - performs transfer between accouncts
          <li>4. Close account - deletes entry from the database
          <li>5. Log out - returns to the initial menu
          <li>0. Exit
        </ls>
 The database used here is SQLite (with sqlite3 module)
 
