// This is not a java source file, use `.java` to color the code.

class Entity {
    static staticData; // Maybe some static data shall be recorded.
    static void changeStaticData(messageData);
    // Data:
    id entityId;
    data dataForLogicJudgement;
    data elseData;
    // Relationship:
    id[] relationships;
    // Running:
    public void listen(data) { // Data is the message we got from other entities.
        switch (data) { // We need to judge the type of data.
            case typeAndSender:
                dataForLogicJudgement = data.dataForLogicJudgement;
                elseData = data.elseData;
                changeStaticData();
                someMessageGot[data] = true; // Change the snapshot.
                if (someLogicMet(someMessageGot, dataForLogicJudgement, staticData)) { // Here is the business role, namely the logic.
                    sendSomeMessages(); // Send messages when meets the business role.
                }
                break;
            case anotherTypeOrSender:
                // Do something.
                break;
            default: // Wrong message.
                break;
        }
    }
    // Interface:
    private sendSomeMessages();
    private sendSomeOtherMessges(); // Interface uses to sending messges to other entities.
    // Snapshot:
    boolean[] someMessageGot;
}
