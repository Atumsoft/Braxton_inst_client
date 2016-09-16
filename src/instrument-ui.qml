import QtQuick 2.0
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.2

ApplicationWindow {
    visible: true
    title: "Atumate Brewing Instruments"
    id: applicationWindow1
    width: 700
    height: 600

    ColumnLayout {
            id: columnLayout2
            anchors.fill: parent

            RowLayout {
                id: rowLayout2
                anchors.horizontalCenter: parent.horizontalCenter

                Label {
                    id: label3
                    text: qsTr("Select Instrument:")
                    anchors.verticalCenter: parent.verticalCenter
                }

                ComboBox{
                    id:instruments
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            RowLayout {
                id: rowLayout1
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 25.6

                ColumnLayout {
                    id: columnLayout1

                    Label {
                        id: label1
                        text: qsTr("Date To Start From:")
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Calendar {
                        id: startDate
                    }

                }

                ColumnLayout {
                    id: columnLayout3

                    Label {
                        id: label2
                        text: qsTr("Date To End On:")
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Calendar {
    		            id: endDate
                    }
                }


            }

            Button {
                id: exportButton
                text: qsTr("Save To Excel")
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
            }
    }

}

