//
//  CourseNavigationView.swift
//  Course
//
//  Created by  Stepanok Ivan on 14.02.2023.
//

import SwiftUI
import Core

struct CourseNavigationView: View {
    
    @ObservedObject private var viewModel: CourseUnitViewModel
    private let sectionName: String

    init(sectionName: String, viewModel: CourseUnitViewModel) {
        self.viewModel = viewModel
        self.sectionName = sectionName
        
    }
    
    var body: some View {
        HStack(alignment: .top, spacing: 24) {
            if viewModel.selectedLesson() == viewModel.blocks.first
                && viewModel.blocks.count != 1 {
                UnitButtonView(type: .first, action: {
                    viewModel.select(move: .next)
                    self.viewModel.createLessonType()
                    self.viewModel.killPlayer.toggle()
                })
            } else {
               
                if viewModel.previousLesson != "" {
                    UnitButtonView(type: .previous, action: {
                        viewModel.select(move: .previous)
                        self.viewModel.createLessonType()
                        self.viewModel.killPlayer.toggle()
                    })
                }
                if viewModel.nextLesson != "" {
                    UnitButtonView(type: .next, action: {
                        viewModel.select(move: .next)
                        self.viewModel.createLessonType()
                        self.viewModel.killPlayer.toggle()
                    })
                }
                if viewModel.selectedLesson() == viewModel.blocks.last {
                    UnitButtonView(type: viewModel.blocks.count == 1 ? .finish : .last, action: {
                        viewModel.router.presentAlert(
                            alertTitle: CourseLocalization.Courseware.goodWork,
                            alertMessage: (CourseLocalization.Courseware.section
                                           + " " + sectionName + " " + CourseLocalization.Courseware.isFinished),
                            action: CourseLocalization.Courseware.backToOutline,
                            image: CoreAssets.goodWork.swiftUIImage,
                            onCloseTapped: {},
                            okTapped: {
                                viewModel.router.dismiss(animated: false)
                                viewModel.router.removeLastView(controllers: 2)
                            }
                        )
                    })
                }
            }
        }.frame(minWidth: 0, maxWidth: .infinity)
            .padding(.horizontal, 24)
            
    }
}

#if DEBUG
struct CourseNavigationView_Previews: PreviewProvider {
    static var previews: some View {
        let viewModel = CourseUnitViewModel(lessonID: "1",
                                            courseID: "1",
                                            blocks: [],
                                            interactor: CourseInteractor.mock,
                                            router: CourseRouterMock(),
                                            connectivity: Connectivity(),
                                            manager: DownloadManagerMock())
        
        CourseNavigationView(sectionName: "Name", viewModel: viewModel)
    }
}
#endif
